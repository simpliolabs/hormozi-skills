"""Contract tests for the additive downstream CRO gate.

Run: python -m unittest discover -s tests -p 'test_cro_waterfall.py'
No network, no model calls and no output file writes.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from cro_gate import choose_cro_gate  # noqa: E402


class GateDecisionTests(unittest.TestCase):
    def test_full_offer_stages_are_eligible_without_explicit_cro(self):
        for stage in ("A", "B", "D"):
            with self.subTest(stage=stage):
                gate = choose_cro_gate(stage)
                self.assertTrue(gate.required)
                self.assertEqual(gate.depth, "readiness")
                self.assertEqual(gate.artifact, "output/CRO_REVIEW.md")

    def test_live_page_is_full_audit(self):
        result = choose_cro_gate("B", surface="live")
        self.assertTrue(result.required)
        self.assertEqual(result.depth, "full_page")

    def test_planned_page_is_readiness_not_fake_qa(self):
        result = choose_cro_gate("A", surface="planned")
        self.assertEqual(result.depth, "readiness")
        self.assertIn("NOT ASSESSED", result.reason)

    def test_offline_offer_still_gets_minimal_handoff(self):
        result = choose_cro_gate("D", surface="offline")
        self.assertTrue(result.required)
        self.assertEqual(result.depth, "buyer_handoff")
        self.assertIn("NOT APPLICABLE", result.reason)

    def test_stage_c_is_conditional_on_digital_conversion(self):
        no_page = choose_cro_gate("C")
        has_page = choose_cro_gate("C", digital_destination=True)
        self.assertFalse(no_page.required)
        self.assertTrue(has_page.required)
        self.assertEqual(has_page.depth, "readiness")

    def test_stage_e_offer_workflow_vs_unrelated_custom_task(self):
        self.assertTrue(choose_cro_gate("E", offer_workflow=True).required)
        self.assertFalse(choose_cro_gate("E", offer_workflow=False).required)

    def test_focused_task_never_forces_full_pipeline(self):
        for stage in ("A", "B", "C", "D", "E"):
            with self.subTest(stage=stage):
                result = choose_cro_gate(stage, surface="live", focused=True, digital_destination=True)
                self.assertFalse(result.required)
                self.assertIsNone(result.artifact)

    def test_unknown_surface_does_not_pretend_live_page(self):
        result = choose_cro_gate("A", surface="unknown")
        self.assertEqual(result.depth, "readiness")
        self.assertNotEqual(result.depth, "full_page")

    def test_invalid_stage_and_surface_fail_closed(self):
        for args in (("F", "live"), ("B", "pretend")):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    choose_cro_gate(args[0], surface=args[1])

    def test_cli_stdout_is_read_only_json(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "cro_gate.py"), "--stage", "C", "--surface", "live", "--digital-destination"],
            capture_output=True, text=True, check=True,
        )
        obj = json.loads(completed.stdout)
        self.assertTrue(obj["required"])
        self.assertEqual(obj["depth"], "full_page")
        self.assertEqual(obj["artifact"], "output/CRO_REVIEW.md")


class RepositoryContractTests(unittest.TestCase):
    def _read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_skill_is_installed_and_has_frontmatter(self):
        skill = self._read("skills/cro-page-optimizer/SKILL.md")
        self.assertTrue(skill.startswith("---\nname: cro-page-optimizer\ndescription:"))
        self.assertIn("default downstream", skill.lower())
        self.assertIn("NOT ASSESSED", skill)
        self.assertTrue((ROOT / "skills/cro-page-optimizer/agents/openai.yaml").is_file())
        self.assertTrue((ROOT / "skills/cro-page-optimizer/references/CRO_FRAMEWORK.md").is_file())

    def test_both_orchestrator_entrypoints_load_cro_method(self):
        for path in ("skills/hormozi-orchestrator/SKILL.md", "agents/hormozi-orchestrator.md"):
            with self.subTest(path=path):
                contents = self._read(path)
                self.assertIn("cro-page-optimizer/SKILL.md", contents)
                self.assertIn("CRO_REVIEW.md", contents)

    def test_shared_waterfall_keeps_existing_review_contract(self):
        doc = self._read("references/orchestration.md")
        waterfall = self._read("references/cro-waterfall.md")
        self.assertIn("Independent-review floor", doc)
        self.assertIn("Fictional fixture; real business validation absent", doc)
        self.assertIn("CRO_REVIEW.md", doc)
        self.assertIn("sub-cro", doc)
        self.assertIn("not a newly supported", doc)
        self.assertIn("first-completion seven-hold", waterfall.lower())
        self.assertIn("root", waterfall.lower())

    def test_readme_has_skill_and_visible_waterfall_art(self):
        readme = self._read("README.md")
        self.assertIn("cro-page-optimizer", readme)
        self.assertIn("cro-waterfall.svg", readme)
        self.assertIn("do **not** need to say", readme)
        self.assertTrue((ROOT / "assets/readme/cro-waterfall.svg").is_file())


if __name__ == "__main__":
    unittest.main()
