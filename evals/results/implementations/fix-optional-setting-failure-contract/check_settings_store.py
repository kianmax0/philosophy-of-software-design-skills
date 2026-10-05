#!/usr/bin/env python3
"""Deterministic checks for SettingsStore's read failure contract."""

import unittest

from settings_store import SettingsStore


class FakeBackend:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def read(self, key):
        if self.error is not None:
            raise self.error
        return self.result


class SettingsStoreChecks(unittest.TestCase):
    def test_missing_optional_key_returns_none(self):
        settings = SettingsStore(FakeBackend(error=KeyError("theme")))
        self.assertIsNone(settings.get_optional("theme"))

    def test_present_optional_key_returns_value(self):
        settings = SettingsStore(FakeBackend(result="dark"))
        self.assertEqual(settings.get_optional("theme"), "dark")

    def test_permission_failure_propagates_from_optional_read(self):
        failure = PermissionError("access denied")
        settings = SettingsStore(FakeBackend(error=failure))
        with self.assertRaises(PermissionError) as raised:
            settings.get_optional("theme")
        self.assertIs(raised.exception, failure)

    def test_transport_failure_propagates_from_optional_read(self):
        failure = ConnectionError("backend unavailable")
        settings = SettingsStore(FakeBackend(error=failure))
        with self.assertRaises(ConnectionError) as raised:
            settings.get_optional("theme")
        self.assertIs(raised.exception, failure)

    def test_required_read_contract_remains_unchanged(self):
        failure = PermissionError("access denied")
        settings = SettingsStore(FakeBackend(error=failure))
        with self.assertRaises(PermissionError) as raised:
            settings.get_required("theme")
        self.assertIs(raised.exception, failure)


if __name__ == "__main__":
    unittest.main(verbosity=2)
