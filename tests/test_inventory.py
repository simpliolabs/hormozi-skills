import json
import shutil
import tempfile
import unittest
from pathlib import Path

import helpers
import check_outputs as co

REPO = helpers.REPO
FIX = json.loads((REPO / "tests" / "fixtures" / "expected_inventory.json").read_text(encoding="utf-8"))


class TestPinnedInventory(unittest.TestCase):
    def test_original_18_skills_and_6_agents_still_present(self):
        skills = sorted(p.parent.name for p in (REPO / "skills").glob("*/SKILL.md"))
        agents = sorted(p.stem for p in (REPO / "agents").glob("*.md"))
        for s in FIX["original_skills"]:
            self.assertIn(s, skills)
        for a in FIX["original_agents"]:
            self.assertIn(a, agents)
        self.assertEqual(len(FIX["original_skills"]), 18)
        self.assertEqual(len(FIX["original_agents"]), 6)
        self.assertEqual(len(FIX["business_skills"]), 17)
        self.assertNotIn("create-plugin", FIX["business_skills"])

    def test_untouched_files_are_byte_identical(self):
        for rel, digest in FIX["unchanged_sha256"].items():
            self.assertEqual(co.protected_text_hash((REPO / rel).read_bytes()), digest, rel)

    def test_protected_text_hash_accepts_lf_and_crlf_only(self):
        lf = b"line one\nline two\n"
        self.assertEqual(co.protected_text_hash(lf), co.protected_text_hash(lf.replace(b"\n", b"\r\n")))
        self.assertNotEqual(co.protected_text_hash(lf), co.protected_text_hash(lf + b"x"))
        self.assertNotEqual(co.protected_text_hash(lf), co.protected_text_hash(b"line one\nline 2wo\n"))

    def test_repo_validation_clean(self):
        self.assertEqual([f for f in co.validate_repo(REPO) if f.severity == "error"], [])


class TestRepoValidatorNegatives(unittest.TestCase):
    def clone(self):
        t = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, t, ignore_errors=True)
        for d in ("skills", "agents", "contracts"):
            shutil.copytree(REPO / d, t / d)
        shutil.copy(REPO / "LICENSE", t / "LICENSE")
        (t / "tests" / "fixtures").mkdir(parents=True)
        shutil.copy(REPO / "tests" / "fixtures" / "expected_inventory.json", t / "tests" / "fixtures")
        return t

    def codes(self, t):
        return {f.code for f in co.validate_repo(t)}

    def test_missing_skill_detected(self):
        t = self.clone(); shutil.rmtree(t / "skills" / "bonus-stack")
        self.assertIn("INVENTORY_MISSING", self.codes(t))

    def test_name_directory_mismatch(self):
        t = self.clone(); p = t / "skills" / "bonus-stack" / "SKILL.md"
        p.write_text(p.read_text(encoding="utf-8").replace("name: bonus-stack", "name: wrong", 1), encoding="utf-8")
        self.assertIn("FRONTMATTER_NAME_MISMATCH", self.codes(t))

    def test_missing_description(self):
        t = self.clone(); p = t / "agents" / "sub-sales.md"
        text = p.read_text(encoding="utf-8")
        import re
        p.write_text(re.sub(r"^description:.*$", "", text, count=1, flags=re.M), encoding="utf-8")
        self.assertIn("FRONTMATTER_INVALID", self.codes(t))

    def test_create_plugin_modified_detected(self):
        t = self.clone(); p = t / "skills" / "create-plugin" / "SKILL.md"
        p.write_text(p.read_text(encoding="utf-8") + "\nextra", encoding="utf-8")
        self.assertIn("PROTECTED_FILE_CHANGED", self.codes(t))

    def test_license_modified_detected(self):
        t = self.clone(); (t / "LICENSE").write_text("not MIT")
        self.assertIn("PROTECTED_FILE_CHANGED", self.codes(t))

    def test_broken_schema_detected(self):
        t = self.clone(); (t / "contracts" / "claims.schema.json").write_text('{"type": 12}')
        self.assertIn("SCHEMA_INVALID", self.codes(t))


if __name__ == "__main__":
    unittest.main()
