"""Minimal structured logging for the twin.

One JSON object per line on stdout, which is what Hugging Face Spaces captures
and shows in the Space logs. No external dependency and no log files to rotate —
just greppable lines you can pull into any viewer later.

    {"event": "request_end", "ts": 1724800000.12, "req_id": "a1b2c3d4",
     "latency_ms": 812, "tool_rounds": 1, "tool_calls": ["record_user_email"],
     "answer_chars": 274, "status": "ok"}
"""

import json
import logging
import time
import uuid

logging.basicConfig(level=logging.INFO, format="%(message)s")
_log = logging.getLogger("twin")


def log_event(event, **fields):
    """Emit one structured log line: {"event": ..., "ts": ..., **fields}."""
    _log.info(json.dumps({"event": event, "ts": round(time.time(), 3), **fields}))


def new_request_id():
    """Short id to correlate the log lines belonging to one visitor turn."""
    return uuid.uuid4().hex[:8]
