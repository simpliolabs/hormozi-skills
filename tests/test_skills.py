"""Evidence/authority preflight: applied to all 17 business skills, methodology preserved."""
import hashlib
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIX = REPO / "tests" / "fixtures"
INV = json.loads((FIX / "expected_inventory.json").read_text(encoding="utf-8"))
BASE = json.loads((FIX / "baseline_skills.json").read_text(encoding="utf-8"))
TARGETED = ["market-research", "hormozi-offer", "audit-offer", "pricing-strategy", "bonus-stack",
            "hormozi-pitch", "hormozi-hooks", "landing-page-copy", "business-model", "objection-destroyer"]
REFS = ["skills/hormozi-hooks/references/hormozi-style-hooks.md", "skills/idea-to-product/references/offer-key-points.md"]
PRE = "## Evidence & Authority Preflight"
SPECIFIC = "## Skill-Specific Evidence Rules"


def read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def block(text):
    """The preflight section: from its heading to the next H2."""
    m = re.search(rf"^{re.escape(PRE)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(0) if m else None


def strip_added(text):
    """Remove the common preflight and the skill-specific section, leaving the original methodology."""
    text = text.replace(block(text) or "", "", 1)
    return re.sub(rf"\n?^{re.escape(SPECIFIC)}\n.*\Z", "", text, flags=re.S | re.M)


def headings(text):
    return [l for l in text.splitlines() if l.startswith("## ")]


class TestPreflightApplied(unittest.TestCase):
    def test_all_17_business_skills_carry_one_identical_preflight(self):
        blocks = set()
        for s in INV["business_skills"]:
            text = read(f"skills/{s}/SKILL.md")
            self.assertEqual(text.count(PRE), 1, s)
            blocks.add(block(text))
        self.assertEqual(len(blocks), 1, "the common preflight must be one shared text")

    def test_preflight_sits_directly_under_the_title(self):
        for s in INV["business_skills"]:
            body = read(f"skills/{s}/SKILL.md").split("---", 2)[2].lstrip()
            lines = [l for l in body.splitlines() if l.strip()]
            self.assertTrue(lines[0].startswith("# "), s)
            self.assertEqual(lines[1], PRE, s)

    def test_create_plugin_and_orchestrator_are_not_given_the_preflight(self):
        self.assertNotIn(PRE, read("skills/create-plugin/SKILL.md"))
        self.assertNotIn(PRE, read("skills/hormozi-orchestrator/SKILL.md"))

    def test_frontmatter_is_unchanged(self):
        for s in INV["business_skills"]:
            fm = read(f"skills/{s}/SKILL.md").split("\n---\n", 1)[0]
            self.assertEqual(sha(fm), BASE[s]["frontmatter_sha256"], s)

    def test_untargeted_skills_keep_methodology_byte_for_byte(self):
        for s in INV["business_skills"]:
            if s in TARGETED:
                continue
            self.assertEqual(sha(strip_added(read(f"skills/{s}/SKILL.md"))), BASE[s]["sha256"], s)

    def test_targeted_skills_keep_every_original_section_heading(self):
        for s in TARGETED:
            now = headings(strip_added(read(f"skills/{s}/SKILL.md")))
            for h in BASE[s]["headings"]:
                self.assertIn(h, now, f"{s} lost section {h}")

    def test_only_targeted_skills_have_skill_specific_rules(self):
        for s in INV["business_skills"]:
            has = SPECIFIC in read(f"skills/{s}/SKILL.md")
            self.assertEqual(has, s in TARGETED, s)

    def test_reference_files_keep_original_text_under_an_evidence_note(self):
        sentinel = "<!-- end evidence note -->\n\n"
        for rel in REFS:
            text = read(rel)
            self.assertIn(sentinel, text, rel)
            note, original = text.split(sentinel, 1)
            self.assertIn("references/evidence-contract.md", note, rel)
            self.assertEqual(sha(original), BASE[rel]["sha256"], f"{rel} original content changed")

    def test_shared_references_exist(self):
        for rel in ("references/evidence-contract.md", "references/commercial-feasibility.md"):
            self.assertTrue((REPO / rel).is_file(), rel)

    def test_every_preflight_pointer_resolves(self):
        for s in INV["business_skills"]:
            for rel in re.findall(r"`(references/[\w./-]+)`", block(read(f"skills/{s}/SKILL.md")) or ""):
                self.assertTrue((REPO / rel).is_file(), f"{s} -> {rel}")


class TestFeasibilityArithmetic(unittest.TestCase):
    """The worked example in the feasibility reference must match the arithmetic."""

    def test_contribution_example_is_computed_not_asserted(self):
        text = read("references/commercial-feasibility.md")
        price, cost = 2500_00, 2200_00
        contribution = price - cost
        pct = round(100 * contribution / price)
        self.assertEqual((contribution, pct), (300_00, 12))
        for needle in ("2,500", "2,200", "300", "12 %"):
            self.assertIn(needle, text)

    def test_missing_cost_inputs_are_named(self):
        text = read("references/commercial-feasibility.md")
        for item in ("CAC", "payment fees", "commissions", "support"):
            self.assertIn(item, text)


if __name__ == "__main__":
    unittest.main()
