"""Original review fixture; the duplication is ownership of a storage contract."""


def make_storage_record(timestamp_seconds, kind):
    """Construct and validate the version-2 storage record contract."""
    timestamp_ms = int(timestamp_seconds * 1000)
    if timestamp_ms < 0:
        raise ValueError("timestamp must be nonnegative")
    return {
        "schema_version": 2,
        "timestamp_ms": timestamp_ms,
        "kind": kind,
    }


def validate_storage_record(record):
    """Validate records at the storage boundary against the same contract."""
    if record["schema_version"] != 2 or not isinstance(record["timestamp_ms"], int):
        raise ValueError("invalid storage record")


def import_sessions(rows, store):
    for row in rows:
        store.write(make_storage_record(row["timestamp_seconds"], "session"))


def import_events(rows, store):
    for row in rows:
        store.write(make_storage_record(row["timestamp_seconds"], "event"))


class Store:
    """Store version-2 records with millisecond timestamps, preserving write order."""

    def __init__(self):
        self.records = []

    def write(self, record):
        validate_storage_record(record)
        self.records.append(record.copy())
