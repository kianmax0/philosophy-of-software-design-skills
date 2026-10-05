"""Original review fixture; the duplication is ownership of a storage contract."""


def import_sessions(rows, store):
    for row in rows:
        timestamp_ms = int(row["timestamp_seconds"] * 1000)
        if timestamp_ms < 0:
            raise ValueError("timestamp must be nonnegative")
        store.write({"schema_version": 2, "timestamp_ms": timestamp_ms, "kind": "session"})


def import_events(rows, store):
    for row in rows:
        timestamp_ms = int(row["timestamp_seconds"] * 1000)
        if timestamp_ms < 0:
            raise ValueError("timestamp must be nonnegative")
        store.write({"schema_version": 2, "timestamp_ms": timestamp_ms, "kind": "event"})


class Store:
    """Store version-2 records with millisecond timestamps, preserving write order."""

    def __init__(self):
        self.records = []

    def write(self, record):
        if record["schema_version"] != 2 or not isinstance(record["timestamp_ms"], int):
            raise ValueError("invalid storage record")
        self.records.append(record.copy())
