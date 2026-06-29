from __future__ import annotations

import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass(slots=True)
class WindowDecision:
    allowed: bool
    remaining: int
    retry_after_seconds: int


@dataclass(slots=True)
class SlidingWindow:
    limit: int
    seconds: int = 60
    events: dict[str, deque[float]] = field(default_factory=lambda: defaultdict(deque))

    def check(self, key: str) -> WindowDecision:
        if self.limit <= 0:
            return WindowDecision(True, 0, 0)
        now = time.monotonic()
        bucket = self.events[key]
        while bucket and now - bucket[0] > self.seconds:
            bucket.popleft()
        if len(bucket) >= self.limit:
            retry_after = max(1, int(self.seconds - (now - bucket[0])))
            return WindowDecision(False, 0, retry_after)
        bucket.append(now)
        return WindowDecision(True, self.limit - len(bucket), 0)


def request_id(existing: str | None = None) -> str:
    return existing or uuid.uuid4().hex
