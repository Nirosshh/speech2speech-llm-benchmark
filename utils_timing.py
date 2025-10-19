
import time
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.monotonic()
    yield lambda: time.monotonic() - start

class FirstTokenTimer:
    def __init__(self):
        self.started_at = None
        self.first_token_at = None

    def start(self):
        import time
        self.started_at = time.monotonic()

    def mark_first_token(self):
        import time
        if self.first_token_at is None:
            self.first_token_at = time.monotonic()

    @property
    def ttfb(self):
        if self.started_at is None or self.first_token_at is None:
            return None
        return self.first_token_at - self.started_at
