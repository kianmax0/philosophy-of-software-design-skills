import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


spec = importlib.util.spec_from_file_location(
    "validate", Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
)
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "skills" / "sample-skill"
        self.folder.mkdir(parents=True)
        fixture = self.root / "evals" / "fixtures" / "sample.py"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("pass\n", encoding="utf-8")
        (self.root / "evals" / "cases.json").write_text(json.dumps([{
            "id": "sample-case",
            "skill": "sample-skill",
            "mode": "review",
            "fixture": "fixtures/sample.py",
            "request": "Review the fixture.",
            "acceptance": ["Use code evidence."],
            "reject": ["Invent behavior."],
        }]), encoding="utf-8")

    def write_skill(self, fields=None, body="# Perform a specific task\n"):
        fields = fields or "name: sample-skill\ndescription: Inspect a concrete caller contract.\n"
        path = self.folder / "SKILL.md"
        path.write_text("---\n{}---\n{}".format(fields, body), encoding="utf-8")
        return path

    def test_valid_package(self):
        self.write_skill()
        skills, errors = validate.validate_repository(self.root)
        self.assertEqual([self.folder], skills)
        self.assertEqual([], errors)

    def test_rejects_duplicate_metadata_keys(self):
        self.write_skill("name: sample-skill\nname: sample-skill\ndescription: Inspect a caller.\n")
        self.assertTrue(validate.validate_skill(self.folder))

    def test_rejects_name_mismatch_and_empty_description(self):
        self.write_skill("name: different-name\ndescription: ''\n")
        self.assertEqual(2, len(validate.validate_skill(self.folder)))

    def test_rejects_non_string_metadata_values(self):
        self.write_skill("name: sample-skill\ndescription: Inspect a caller.\nmetadata:\n  version: 1\n")
        self.assertTrue(validate.validate_skill(self.folder))

    def test_mit_skill_bundles_its_license(self):
        self.write_skill("name: sample-skill\ndescription: Inspect a caller.\nlicense: MIT\n")
        self.assertTrue(validate.validate_skill(self.folder))
        (self.folder / "LICENSE").write_text("MIT License", encoding="utf-8")
        self.assertEqual([], validate.validate_skill(self.folder))

    def test_skill_links_cannot_depend_on_repository_siblings(self):
        outside = self.root / "shared.md"
        outside.write_text("Shared guide", encoding="utf-8")
        path = self.write_skill(body="[shared](../../shared.md)\n")
        self.assertTrue(validate.validate_links(path, self.root, self.folder))

    def test_local_reference_must_exist(self):
        path = self.write_skill(body="[reference](references/guide.md)\n")
        self.assertTrue(validate.validate_links(path, self.root, self.folder))
        reference = self.folder / "references" / "guide.md"
        reference.parent.mkdir()
        reference.write_text("Guide", encoding="utf-8")
        self.assertEqual([], validate.validate_links(path, self.root, self.folder))

    def test_external_and_anchor_links_need_no_network(self):
        path = self.write_skill(body="[source](https://example.org/guide) [section](#example)\n")
        self.assertEqual([], validate.validate_links(path, self.root, self.folder))

    def test_missing_skill_body_and_malformed_yaml(self):
        self.write_skill(body="")
        self.assertTrue(validate.validate_skill(self.folder))
        self.write_skill("name: [broken\n")
        self.assertTrue(validate.validate_skill(self.folder))


class FixtureBehaviorTests(unittest.TestCase):
    def test_importers_preserve_record_shape_conversion_and_write_order(self):
        import importlib.util

        path = Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "importers.py"
        fixture_spec = importlib.util.spec_from_file_location("importers_fixture", path)
        fixture = importlib.util.module_from_spec(fixture_spec)
        fixture_spec.loader.exec_module(fixture)
        store = fixture.Store()

        fixture.import_sessions([{"timestamp_seconds": 1.25}, {"timestamp_seconds": 2}], store)
        fixture.import_events([{"timestamp_seconds": 3}], store)

        self.assertEqual(
            [
                {"schema_version": 2, "timestamp_ms": 1250, "kind": "session"},
                {"schema_version": 2, "timestamp_ms": 2000, "kind": "session"},
                {"schema_version": 2, "timestamp_ms": 3000, "kind": "event"},
            ],
            store.records,
        )

    def test_gateway_checks_permission_before_reading_storage(self):
        import importlib.util

        path = Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "document_gateway.py"
        fixture_spec = importlib.util.spec_from_file_location("gateway_fixture", path)
        fixture = importlib.util.module_from_spec(fixture_spec)
        fixture_spec.loader.exec_module(fixture)
        calls = []

        class Permissions:
            def require_read(self, actor, document_id):
                calls.append(("authorize", actor, document_id))

        class Store:
            def read(self, document_id):
                calls.append(("read", document_id))
                return b"document"

        result = fixture.DocumentGateway(Store(), Permissions()).read("alice", "doc-7")

        self.assertEqual(b"document", result)
        self.assertEqual([("authorize", "alice", "doc-7"), ("read", "doc-7")], calls)

    def test_settings_fixture_reproduces_operational_failure_masking(self):
        import importlib.util

        path = Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "settings_store.py"
        fixture_spec = importlib.util.spec_from_file_location("settings_fixture", path)
        fixture = importlib.util.module_from_spec(fixture_spec)
        fixture_spec.loader.exec_module(fixture)

        class Backend:
            def read(self, key):
                raise PermissionError("credential expired")

        # This is the intentional review target: operational failure is mistaken for absence.
        self.assertIsNone(fixture.SettingsStore(Backend()).get_optional("theme"))


class EvaluationCorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "skills").mkdir()
        self.skill_names = {"posd-one", "posd-two"}
        for name in self.skill_names:
            folder = self.root / "skills" / name
            folder.mkdir()
            (folder / "SKILL.md").write_text("skill", encoding="utf-8")
        (self.root / "evals" / "fixtures").mkdir(parents=True)
        (self.root / "evals" / "fixtures" / "sample.py").write_text("pass\n", encoding="utf-8")
        (self.root / "evals" / "cases.json").write_text("[]", encoding="utf-8")

    def write_cases(self, cases):
        import json
        (self.root / "evals" / "cases.json").write_text(json.dumps(cases), encoding="utf-8")

    def case(self, case_id="case-one", skill="posd-one", fixture="fixtures/sample.py"):
        return {
            "id": case_id,
            "skill": skill,
            "mode": "review",
            "fixture": fixture,
            "request": "Inspect the supplied code and recommend a bounded change.",
            "acceptance": ["Cites the relevant behavior in the fixture."],
            "reject": ["Claims behavior not shown by the fixture."],
        }

    def test_valid_corpus_covers_every_skill(self):
        self.write_cases([self.case(case_id=name, skill=name) for name in sorted(self.skill_names)])
        self.assertEqual([], validate.validate_evaluation_cases(self.root))

    def test_duplicate_case_ids_are_rejected(self):
        self.write_cases([self.case(), self.case(skill="posd-two")])
        errors = validate.validate_evaluation_cases(self.root)
        self.assertTrue(any("duplicate case id" in error for error in errors), errors)

    def test_missing_fixture_and_unknown_skill_are_rejected(self):
        case = self.case(skill="posd-missing", fixture="fixtures/missing.py")
        self.write_cases([case])
        errors = validate.validate_evaluation_cases(self.root)
        self.assertTrue(any("unknown skill" in error for error in errors), errors)
        self.assertTrue(any("missing fixture" in error for error in errors), errors)

    def test_uncovered_skills_and_incomplete_criteria_are_rejected(self):
        case = self.case()
        case["acceptance"] = []
        case.pop("reject")
        self.write_cases([case])
        errors = validate.validate_evaluation_cases(self.root)
        self.assertTrue(any("does not cover skills: posd-two" in error for error in errors), errors)
        self.assertTrue(any("acceptance" in error for error in errors), errors)
        self.assertTrue(any("reject" in error for error in errors), errors)

    def test_unknown_case_mode_is_rejected(self):
        self.write_cases([self.case(skill="posd-one"), self.case(case_id="case-two", skill="posd-two")])
        cases = json.loads((self.root / "evals" / "cases.json").read_text(encoding="utf-8"))
        cases[0]["mode"] = "summary"
        self.write_cases(cases)
        errors = validate.validate_evaluation_cases(self.root)
        self.assertTrue(any("mode must be review or implementation" in error for error in errors), errors)

    def test_non_string_modes_are_reported_without_crashing(self):
        for mode in (["review"], {"mode": "review"}, None, 1):
            with self.subTest(mode=mode):
                case = self.case()
                case["mode"] = mode
                self.write_cases([case, self.case(case_id="case-two", skill="posd-two")])
                errors = validate.validate_evaluation_cases(self.root)
                self.assertTrue(any("mode must be review or implementation" in error for error in errors), errors)

    def test_task_export_hides_criteria_and_semantic_case_ids(self):
        case = self.case(case_id="absence-is-not-failure")
        self.write_cases([case, self.case(case_id="case-two", skill="posd-two")])
        script = Path(__file__).resolve().parents[1] / "scripts/prepare_eval.py"
        result = subprocess.run(
            [sys.executable, str(script), case["id"], "--root", str(self.root)],
            capture_output=True, text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual({"id", "skill_path", "mode", "request", "raw_fixture", "fixture_name"}, set(payload))
        self.assertNotIn(case["id"], payload["id"])
        self.assertEqual(case["request"], payload["request"])
        self.assertEqual("pass\n", payload["raw_fixture"])

    def test_fixture_path_cannot_escape_evals(self):
        case = self.case(fixture="../../outside.py")
        self.write_cases([case, self.case(case_id="case-two", skill="posd-two")])
        errors = validate.validate_evaluation_cases(self.root)
        self.assertTrue(any("escapes evals directory" in error for error in errors), errors)

    def test_absolute_fixture_paths_are_not_portable(self):
        case = self.case(fixture=str((self.root / "evals/fixtures/sample.py").resolve()))
        self.write_cases([case, self.case(case_id="case-two", skill="posd-two")])
        errors = validate.validate_evaluation_cases(self.root)
        self.assertTrue(any("fixture must be a relative path" in error for error in errors), errors)

    def test_malformed_cases_json_is_reported(self):
        (self.root / "evals" / "cases.json").write_text("{oops", encoding="utf-8")
        errors = validate.validate_evaluation_cases(self.root)
        self.assertTrue(any("invalid cases.json" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
