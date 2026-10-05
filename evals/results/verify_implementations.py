#!/usr/bin/env python3
"""Independent contract checks for the retained agent implementation artifacts."""

import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


original = load_module("original_importers", HERE.parent / "fixtures/importers.py")
candidate = load_module(
    "candidate_importers",
    HERE / "implementations/centralize-versioned-record-construction/importers.py",
)
settings = load_module(
    "candidate_settings",
    HERE / "implementations/fix-optional-setting-failure-contract/settings_store.py",
)


class ImplementationContracts(unittest.TestCase):
    def test_importer_results_and_partial_effects_match_original(self):
        scenarios = [
            [],
            [{"timestamp_seconds": 1.2349}, {"timestamp_seconds": 0}],
            [{"timestamp_seconds": -0.0001}],
            [{"timestamp_seconds": -0.0011}],
            [{"timestamp_seconds": 2}, {"timestamp_seconds": -1}],
            [{"timestamp_seconds": 2}, {}],
            [{"timestamp_seconds": "bad"}],
            [{"timestamp_seconds": None}],
        ]

        def run(module, name, rows):
            store = module.Store()
            try:
                getattr(module, name)(rows, store)
            except Exception as error:
                return store.records, type(error), str(error)
            return store.records, None, None

        for name in ("import_sessions", "import_events"):
            for rows in scenarios:
                with self.subTest(importer=name, rows=rows):
                    self.assertEqual(run(original, name, rows), run(candidate, name, rows))

    def test_legacy_storage_boundary_is_preserved(self):
        # Existing raw-record callers remain compatible, including behavior
        # that these artifacts do not strengthen (kind or sign validation).
        for record in (
            {"schema_version": 2, "timestamp_ms": 7, "kind": "other"},
            {"schema_version": 2, "timestamp_ms": -7, "kind": "event"},
            {"schema_version": 1, "timestamp_ms": 7, "kind": "event"},
            {"schema_version": 2, "timestamp_ms": "7", "kind": "event"},
        ):
            observed = []
            for module in (original, candidate):
                store = module.Store()
                try:
                    store.write(record)
                except Exception as error:
                    observed.append((store.records, type(error), str(error)))
                else:
                    record_copy = record.copy()
                    record["extra"] = "caller mutation"
                    self.assertEqual([record_copy], store.records)
                    record.pop("extra")
                    observed.append((store.records, None, None))
            self.assertEqual(*observed)

    def test_settings_absence_values_and_required_read(self):
        class Backend:
            def read(self, key):
                return {"theme": "dark", "false": False, "zero": 0, "empty": ""}[key]

        store = settings.SettingsStore(Backend())
        self.assertIsNone(store.get_optional("missing"))
        with self.assertRaises(KeyError):
            store.get_required("missing")
        for key, value in (("theme", "dark"), ("false", False), ("zero", 0), ("empty", "")):
            self.assertEqual(value, store.get_optional(key))
        self.assertEqual("dark", settings.load_theme(store))

    def test_operational_failure_object_and_cause_reach_callers(self):
        for kind in (PermissionError, ConnectionError):
            cause = RuntimeError("underlying cause")
            failure = kind("backend failure")
            failure.__cause__ = cause

            class Backend:
                def read(self, key):
                    raise failure

            store = settings.SettingsStore(Backend())
            for read in (lambda: store.get_optional("theme"),
                         lambda: store.get_required("theme"),
                         lambda: settings.load_theme(store)):
                with self.assertRaises(kind) as caught:
                    read()
                self.assertIs(failure, caught.exception)
                self.assertIs(cause, caught.exception.__cause__)


if __name__ == "__main__":
    unittest.main(verbosity=2)
