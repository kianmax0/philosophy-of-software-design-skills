"""A correct linear search with no demonstrated performance target."""


def find_item(items, requested_id):
    for item in items:
        if item["id"] == requested_id:
            return item
    return None


def find_items(items, requested_ids):
    return [find_item(items, requested_id) for requested_id in requested_ids]
