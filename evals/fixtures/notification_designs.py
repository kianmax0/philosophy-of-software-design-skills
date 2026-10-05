"""Two meaningful notification designs with different delivery guarantees."""


class InlineNotifier:
    """Sends synchronously; the caller sees delivery failures immediately."""

    def __init__(self, transport):
        self._transport = transport

    def notify(self, user_id, message):
        self._transport.send(user_id, message)


class QueuedNotifier:
    """Accepts a message for later delivery; acceptance is not delivery."""

    def __init__(self, queue):
        self._queue = queue

    def notify(self, user_id, message):
        self._queue.enqueue({"user_id": user_id, "message": message})
