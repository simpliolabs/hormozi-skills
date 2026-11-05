"""Routing and onboarding contract tests.

These are documentation and deterministic routing checks, not native auto-activation
or model-usage measurements. Run as part of the existing repository unittest suite.
"""
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from cro_gate import choose_cro_gate  # noqa: E402


class AdaptiveRouteTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_beginner_and_expert_examples_are_visible(self):
        readme = self.read("README.md")
        guide = self.read("docs/START_HERE.md")
        for txt in (readme, guide):
            self.assertIn("business idea", txt)
            self.assertIn("five hooks", txt)
        self.assertIn("choose-your-path.svg", readme)
        self.assertTrue((ROOT / "assets/readme/choose-your-path.svg").is_file())
        self.assertIn("not guaranteed", readme)

    def test_both_entrypoints_require_adaptive_routing(self):
        for path in ("skills/hormozi-orchestrator/SKILL.md", "agents/hormozi-orchestrator.md"):
            with self.subTest(path=path):
                txt = self.read(path)
                self.assertIn("<plugin_root>/references/adaptive-routing.md", txt)
                self.assertIn("one", txt.lower())
                self.assertIn("cro", txt.lower())

    def test_shared_workflow_explicitly_keeps_selective_graph(self):
        txt = self.read("references/orchestration.md")
        guidance = self.read("references/adaptive-routing.md")
        self.assertIn("<plugin_root>/references/adaptive-routing.md", txt)
        self.assertIn("smallest", txt.lower())
        self.assertIn("QUICK", guidance)
        self.assertIn("GUIDED", guidance)
        self.assertIn("DEEP", guidance)
        self.assertIn("not a guaranteed", guidance.lower())

    def test_single_task_does_not_become_a_full_run(self):
        for stage in ("A", "B", "C", "D", "E"):
            with self.subTest(stage=stage):
                result = choose_cro_gate(stage, surface="live", focused=True, digital_destination=True)
                self.assertFalse(result.required)
                self.assertIsNone(result.artifact)

    def test_multi_step_full_offer_still_has_downstream_cro(self):
        for stage in ("A", "B", "D", "E"):
            with self.subTest(stage=stage):
                self.assertTrue(choose_cro_gate(stage).required)
        self.assertTrue(choose_cro_gate("C", digital_destination=True).required)

    def test_no_unsafe_token_cost_promise(self):
        guide = self.read("references/adaptive-routing.md")
        self.assertIn("not enforceable API token limits", guide)
        self.assertIn("unknown", guide)
        self.assertIn("Do not drop evidence checks", guide)

    def test_no_unproven_offer_alias_claim(self):
        guide = self.read("docs/START_HERE.md")
        self.assertIn("proposal", guide.lower())
        self.assertIn("/offer", guide)
        self.assertIn("not guaranteed", guide.lower())


if __name__ == "__main__":
    unittest.main()
