"""Names whose meaning is unclear at their actual call sites."""


def process(rows, flag=False):
    selected = [row for row in rows if row.get("active")]
    if flag:
        return [row["email"] for row in selected]
    return [row["id"] for row in selected]


def load(path):
    """Reads JSON bytes from a local path and returns decoded records."""
    import json

    with open(path, "r", encoding="utf-8") as source:
        return json.load(source)
