"""Original negative fixture; a small boundary owns an authorization invariant."""


class DocumentGateway:
    def __init__(self, store, permissions):
        self._store = store
        self._permissions = permissions

    def read(self, actor, document_id):
        """Return bytes only when actor has read permission; never reveal denied content."""
        self._permissions.require_read(actor, document_id)
        return self._store.read(document_id)


def read_for_download(gateway, actor, document_id):
    return gateway.read(actor, document_id)


def read_for_preview(gateway, actor, document_id):
    return gateway.read(actor, document_id)
