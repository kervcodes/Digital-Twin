"""Per-session sliding-window rate limit.

The Space runs on a personal OpenAI key behind a public URL. `max_completion_tokens`
caps the size of one answer; it does nothing about volume. This caps how many
turns one visitor can take in a rolling window so a scripted loop can't run up
the bill.

In-memory only: state resets when the Space restarts, and it is not shared
across replicas. That is acceptable for a single-replica personal Space — the
goal is to blunt abuse, not to meter usage exactly.

Tune without a redeploy via env vars:
    RATE_LIMIT_MAX          max turns per window   (default 20)
    RATE_LIMIT_WINDOW_SEC   window length, seconds (default 60)
"""

import os
import threading
import time

MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX", "20"))
WINDOW_SEC = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))

_hits: dict[str, list[float]] = {}
_lock = threading.Lock()


def check(key):
    """Record a hit for `key` and report whether it is allowed.

    Returns (allowed, retry_after_seconds). When not allowed, no hit is
    recorded, so a blocked visitor doesn't push their own window forward.
    """
    now = time.monotonic()
    cutoff = now - WINDOW_SEC
    with _lock:
        hits = [t for t in _hits.get(key, ()) if t > cutoff]
        if len(hits) >= MAX_REQUESTS:
            _hits[key] = hits
            retry_after = int(hits[0] + WINDOW_SEC - now) + 1
            return False, min(WINDOW_SEC, max(1, retry_after))
        hits.append(now)
        _hits[key] = hits
        _sweep(cutoff)
        return True, 0


def _sweep(cutoff):
    """Drop keys whose hits have all expired. Called under _lock."""
    if len(_hits) <= 512:
        return
    for key in [k for k, v in _hits.items() if not v or v[-1] <= cutoff]:
        del _hits[key]
