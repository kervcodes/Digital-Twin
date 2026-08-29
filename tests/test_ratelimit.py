"""Tests for the per-session rate limiter.

Pure logic, no network, no OpenAI. Run with:  python -m unittest -v
"""

import os
import unittest

os.environ.setdefault("RATE_LIMIT_MAX", "3")
os.environ.setdefault("RATE_LIMIT_WINDOW_SEC", "60")

import ratelimit  # noqa: E402  (import after env is set)


class RateLimitTest(unittest.TestCase):
    def setUp(self):
        ratelimit._hits.clear()
        self._real_monotonic = ratelimit.time.monotonic
        self._now = 1000.0
        ratelimit.time.monotonic = lambda: self._now

    def tearDown(self):
        ratelimit.time.monotonic = self._real_monotonic

    def test_allows_up_to_the_limit_then_blocks(self):
        results = [ratelimit.check("sess")[0] for _ in range(4)]
        self.assertEqual(results, [True, True, True, False])

    def test_blocked_call_does_not_consume_budget(self):
        for _ in range(3):
            ratelimit.check("sess")
        # Two blocked attempts...
        self.assertFalse(ratelimit.check("sess")[0])
        self.assertFalse(ratelimit.check("sess")[0])
        # ...then the window rolls and exactly the limit is available again,
        # not fewer — the blocked attempts recorded nothing.
        self._now += 61
        results = [ratelimit.check("sess")[0] for _ in range(4)]
        self.assertEqual(results, [True, True, True, False])

    def test_keys_are_independent(self):
        for _ in range(3):
            self.assertTrue(ratelimit.check("a")[0])
        self.assertFalse(ratelimit.check("a")[0])
        self.assertTrue(ratelimit.check("b")[0])

    def test_window_expiry_frees_capacity(self):
        for _ in range(3):
            ratelimit.check("sess")
        self.assertFalse(ratelimit.check("sess")[0])
        self._now += 60.1
        self.assertTrue(ratelimit.check("sess")[0])

    def test_retry_after_is_bounded(self):
        for _ in range(3):
            ratelimit.check("sess")
        allowed, retry_after = ratelimit.check("sess")
        self.assertFalse(allowed)
        self.assertGreaterEqual(retry_after, 1)
        self.assertLessEqual(retry_after, ratelimit.WINDOW_SEC)


if __name__ == "__main__":
    unittest.main()
