"""A stale comment and two units that must remain distinguishable."""


def expire_at(deadline_ms, now_ms):
    # Convert deadline from seconds to milliseconds before comparing.
    return now_ms >= deadline_ms


def retry_delay_ms(attempt):
    """Return a delay in milliseconds for exponential backoff."""
    return min(100 * (2**attempt), 5_000)


def retry_delay_seconds(attempt):
    """Return a delay in seconds for a human-readable status message."""
    return min(2**attempt, 30)
