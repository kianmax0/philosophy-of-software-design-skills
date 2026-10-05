"""Original error-contract fixture; absence and other failures are distinct."""


class SettingsStore:
    def __init__(self, backend):
        self._backend = backend

    def get_required(self, key):
        """Read a setting; backend raises KeyError if missing, other errors on failure."""
        return self._backend.read(key)

    def get_optional(self, key):
        """Return None when a setting is absent. Stored values are never None."""
        try:
            return self.get_required(key)
        except KeyError:
            return None


def load_theme(settings):
    value = settings.get_optional("theme")
    return "system" if value is None else value
