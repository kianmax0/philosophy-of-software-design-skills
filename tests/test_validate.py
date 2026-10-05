import importlib.util
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


if __name__ == "__main__":
    unittest.main()
