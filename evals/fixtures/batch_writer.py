"""Callers repeat batch ordering and retry rules; some differences are meaningful."""


def write_events(events, sink):
    for event in events:
        if not event.get("id"):
            raise ValueError("event id is required")
    for attempt in range(3):
        try:
            sink.write_many(events)
            return
        except TimeoutError:
            if attempt == 2:
                raise


def write_audit_records(records, sink):
    for record in records:
        if not record.get("actor"):
            raise ValueError("audit actor is required")
    for attempt in range(3):
        try:
            sink.write_many(records)
            return
        except TimeoutError:
            if attempt == 2:
                raise


def write_payment_batch(payments, sink):
    """Payments are intentionally submitted once; the sink is not idempotent."""
    for payment in payments:
        if payment["amount_cents"] <= 0:
            raise ValueError("payment amount must be positive")
    sink.write_many(payments)
