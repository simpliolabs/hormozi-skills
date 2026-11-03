"""Declared A-E task/receipt dependency checks, run against real task graphs and file bytes."""
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import build_run, codes, read_json, write_json, sha
import check_outputs as co

SRC = "input/offer.md"
OFFER, DIAG, CHECK = "output/OFFER.md", "output/ORIGINAL_OFFER_AUDIT.md", "output/REVISED_OFFER_CHECK.md"
PRICING = "output/PRICING.md"

# (id, role, mode, depends_on, write_set)
B_ROUTE = [
    ("t_diag", "sub-value", "diagnostic", [], [DIAG]),
    ("t_rev", "sub-offer", "revision", ["t_diag"], [OFFER]),
    ("t_check", "sub-value", "revised_check", ["t_rev"], [CHECK]),
    ("t_price", "sub-pricing", "final_feasibility", ["t_rev", "t_check"], [PRICING]),
    ("t_sales", "sub-sales", "copy", ["t_price"], ["output/PITCH.md"]),
]
D_ROUTE = [
    ("t_pkg", "sub-pricing", "packaging_exploration", [], ["output/PACKAGING.md"]),
    ("t_rev", "sub-offer", "revision", ["t_pkg"], [OFFER]),
    ("t_price", "sub-pricing", "final_feasibility", ["t_rev"], [PRICING]),
    ("t_sales", "sub-sales", "copy", ["t_price"], ["output/PITCH.md"]),
]
A_ROUTE = [
    ("t_prop", "sub-offer", "proposal", [], [OFFER]),
    ("t_aud", "sub-value", "audit", ["t_prop"], ["output/OFFER_AUDIT.md"]),
    ("t_price", "sub-pricing", "final_feasibility", ["t_prop", "t_aud"], [PRICING]),
    ("t_sales", "sub-sales", "copy", ["t_price"], ["output/PITCH.md"]),
]
C_ROUTE = [
    ("t_offer", "sub-offer", None, [], []),
    ("t_sales", "sub-sales", "copy", ["t_offer"], ["output/PITCH.md"]),
]


class RouteCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.run_dir, self.ws = build_run(self.tmp)

    def graph(self, stage, route, status=None):
        """Rewrite the task graph; freeze inputs from the real bytes of declared dependencies."""
        status = status or {}
        src = {"path": SRC, "sha256": sha((self.ws / SRC).read_bytes())}
        brief = read_json(self.run_dir / "BRIEF.json")
        brief["stage"] = stage
        write_json(self.run_dir / "BRIEF.json", brief)
        st = read_json(self.run_dir / "RUN_STATE.json")
        by_id, tasks = {}, []
        for tid, role, mode, deps, writes in route:
            for w in writes:
                if w != "output/PITCH.md":
                    (self.ws / w).write_text(f"content of {tid}", encoding="utf-8")
            inputs = [dict(src)] if not deps else []
            for d in (d for d in deps if d in by_id):
                for w in by_id[d]["write_set"]:
                    inputs.append({"path": w, "sha256": sha((self.ws / w).read_bytes())})
            t = {"id": tid, "role": role, "status": status.get(tid, "done"), "depends_on": deps,
                 "inputs": inputs, "write_set": writes}
            if mode:
                t["mode"] = mode
            by_id[tid] = t
            tasks.append(t)
        st["tasks"] = tasks
        write_json(self.run_dir / "RUN_STATE.json", st)
        return st

    def edit(self, fn):
        st = read_json(self.run_dir / "RUN_STATE.json")
        fn(st)
        write_json(self.run_dir / "RUN_STATE.json", st)

    def task(self, st, tid):
        return next(t for t in st["tasks"] if t["id"] == tid)

    def found(self, mode="ready"):
        return codes(co.validate_run(self.run_dir, self.ws, mode))


class TestRoutesPass(RouteCase):
    def test_each_declared_route_is_clean(self):
        for stage, route in (("A", A_ROUTE), ("B", B_ROUTE), ("D", D_ROUTE)):
            with self.subTest(stage=stage):
                self.graph(stage, route)
                self.assertEqual(self.found(), set())

    def test_stage_c_copy_only_with_unrequested_upstream_is_clean(self):
        self.graph("C", C_ROUTE, {"t_offer": "not_applicable"})
        self.assertEqual(self.found(), set())

    def test_focused_stage_e_needs_no_pipeline(self):
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"])])
        self.assertEqual(self.found(), set())


class TestStageB(RouteCase):
    def test_revision_may_not_precede_original_audit(self):
        self.graph("B", B_ROUTE)
        self.edit(lambda s: self.task(s, "t_rev").__setitem__("depends_on", []))
        self.assertIn("ROUTE_ORDER_VIOLATION", self.found())

    def test_revised_check_must_follow_revision(self):
        self.graph("B", B_ROUTE)
        self.edit(lambda s: self.task(s, "t_check").__setitem__("depends_on", ["t_diag"]))
        self.assertIn("ROUTE_ORDER_VIOLATION", self.found())

    def test_final_pricing_must_follow_revised_check(self):
        self.graph("B", B_ROUTE)
        self.edit(lambda s: self.task(s, "t_price").__setitem__("depends_on", ["t_rev"]))
        self.assertIn("ROUTE_ORDER_VIOLATION", self.found())

    def test_original_and_revised_audit_may_not_share_a_file(self):
        self.graph("B", B_ROUTE)
        self.edit(lambda s: self.task(s, "t_check").__setitem__("write_set", [DIAG]))
        self.assertIn("WRITE_SET_OVERLAP", self.found())

    def test_diagnostic_must_read_the_frozen_original(self):
        self.graph("B", B_ROUTE)
        other = self.ws / "output" / "OFFER.md"
        other.write_text("stale pre-existing offer", encoding="utf-8")
        self.edit(lambda s: self.task(s, "t_diag").__setitem__(
            "inputs", [{"path": "output/OFFER.md", "sha256": sha(other.read_bytes())}]))
        self.assertIn("ORIGINAL_SNAPSHOT_NOT_AUDITED", self.found())

    def test_missing_revised_check_is_held_in_ready(self):
        self.graph("B", [r for r in B_ROUTE if r[0] != "t_check"])
        self.edit(lambda s: self.task(s, "t_price").__setitem__("depends_on", ["t_rev"]))
        self.assertIn("ROUTE_TASK_MISSING", self.found())

    def test_draft_tolerates_missing_later_stage(self):
        self.graph("B", B_ROUTE[:2])
        self.assertNotIn("ROUTE_TASK_MISSING", self.found("draft"))
        self.assertIn("ROUTE_TASK_MISSING", self.found("ready"))


class TestStageD(RouteCase):
    def test_final_economics_must_follow_scope_change(self):
        self.graph("D", D_ROUTE)
        self.edit(lambda s: self.task(s, "t_price").__setitem__("depends_on", ["t_pkg"]))
        self.assertIn("ROUTE_ORDER_VIOLATION", self.found())

    def test_packaging_exploration_cannot_stand_in_for_final_pricing(self):
        self.graph("D", [r for r in D_ROUTE if r[0] != "t_price"])
        self.edit(lambda s: self.task(s, "t_sales").__setitem__("depends_on", ["t_rev"]))
        self.assertIn("ROUTE_TASK_MISSING", self.found())


class TestStageAandC(RouteCase):
    def test_pricing_before_offer_proposal_rejected(self):
        self.graph("A", A_ROUTE)
        self.edit(lambda s: self.task(s, "t_price").__setitem__("depends_on", []))
        self.assertIn("ROUTE_ORDER_VIOLATION", self.found())

    def test_copy_before_final_pricing_rejected(self):
        self.graph("A", A_ROUTE)
        self.edit(lambda s: self.task(s, "t_sales").__setitem__("depends_on", ["t_aud"]))
        self.assertIn("ROUTE_ORDER_VIOLATION", self.found())

    def test_copy_only_route_cannot_rework_terms(self):
        self.graph("C", C_ROUTE)  # t_offer is "done": offer work happened inside a copy-only run
        self.assertIn("ROUTE_COPY_ONLY_REWORKS_TERMS", self.found())

    def test_copy_only_route_needs_a_sales_task(self):
        self.graph("C", [("t_offer", "sub-offer", None, [], [])], {"t_offer": "not_applicable"})
        self.assertIn("ROUTE_TASK_MISSING", self.found())


class TestInputsAndReceipts(RouteCase):
    def test_dependency_output_must_be_frozen_as_input(self):
        self.graph("B", B_ROUTE)
        self.edit(lambda s: self.task(s, "t_price").__setitem__("inputs", []))
        self.assertIn("INPUT_UNBOUND", self.found())

    def test_input_not_from_a_dependency_or_source_is_rejected(self):
        self.graph("B", B_ROUTE)
        old = self.ws / "output" / "BONUSES.md"
        old.write_text("leftover from another run", encoding="utf-8")
        self.edit(lambda s: self.task(s, "t_price")["inputs"].append(
            {"path": "output/BONUSES.md", "sha256": sha(old.read_bytes())}))
        self.assertIn("INPUT_UNDECLARED", self.found())

    def test_upstream_artifact_changed_after_downstream_froze_it(self):
        self.graph("B", B_ROUTE)
        (self.ws / OFFER).write_text("revised again after pricing", encoding="utf-8")
        self.assertIn("TASK_INPUT_HASH_MISMATCH", self.found())

    def test_not_requested_dependency_needs_no_input(self):
        self.graph("B", B_ROUTE)
        self.edit(lambda s: (self.task(s, "t_price")["inputs"].clear(),
                             self.task(s, "t_price").__setitem__("depends_on", ["t_check"]),
                             self.task(s, "t_check").__setitem__("status", "not_requested")))
        self.assertNotIn("INPUT_UNBOUND", self.found())

    def _receipts(self, qa="pass"):
        out = self.ws / "output"
        cp, qr = out / "CHECKPOINT.md", out / "QA_REPORT.md"
        cp.write_text("checkpoint", encoding="utf-8")
        qr.write_text("qa", encoding="utf-8")
        self.edit(lambda s: s.update(
            checkpoint={"path": "output/CHECKPOINT.md", "sha256": sha(cp.read_bytes()), "decision_version": 3},
            qa_receipt={"path": "output/QA_REPORT.md", "sha256": sha(qr.read_bytes()), "decision_version": 3},
            qa_result=qa))
        return cp, qr

    def test_bound_checkpoint_and_qa_receipt_pass(self):
        self._receipts()
        self.assertEqual(self.found(), set())

    def test_edited_checkpoint_is_stale(self):
        cp, _ = self._receipts()
        cp.write_text("edited after binding", encoding="utf-8")
        self.assertIn("CHECKPOINT_STALE", self.found())

    def test_edited_qa_report_is_stale(self):
        _, qr = self._receipts()
        qr.write_text("edited after binding", encoding="utf-8")
        self.assertIn("QA_RECEIPT_STALE", self.found())

    def test_qa_pass_without_receipt_rejected(self):
        self.edit(lambda s: s.__setitem__("qa_result", "pass"))
        self.assertIn("QA_RECEIPT_MISSING", self.found())

    def test_receipt_for_older_decision_version_is_stale(self):
        self._receipts()
        self.edit(lambda s: s["qa_receipt"].__setitem__("decision_version", 2))
        self.assertIn("QA_RECEIPT_STALE", self.found())

    def test_checkpoint_outside_workspace_rejected(self):
        self._receipts()
        self.edit(lambda s: s["checkpoint"].__setitem__("path", "../elsewhere/CHECKPOINT.md"))
        self.assertIn("PATH_ESCAPE", self.found())


REPO = Path(__file__).resolve().parents[1]
LEGACY_OUTPUTS = {
    "MARKET_RESEARCH", "OFFER", "OFFER_ANGLES", "OFFER_AUDIT", "ORIGINAL_OFFER_AUDIT", "REVISED_OFFER_CHECK",
    "VALUE_PERCEPTION", "BONUS_STACK", "PRICING", "OBJECTIONS", "PRODUCTIZATION", "PACKAGING",
    "PITCH", "HOOKS", "LANDING_PAGE", "SUMMARY", "CHECKPOINT", "QA_REPORT",
}


class TestAdaptersResolve(unittest.TestCase):
    """Referential integrity: whatever the adapters point at must exist and be legal."""

    def agent_texts(self):
        return {p.stem: p.read_text(encoding="utf-8") for p in (REPO / "agents").glob("*.md")}

    def test_every_referenced_skill_and_reference_exists(self):
        for name, text in self.agent_texts().items():
            for rel in re.findall(r"`((?:skills|references)/[\w./-]+)`", text):
                self.assertTrue((REPO / rel).exists(), f"{name} points at missing {rel}")

    def test_every_output_name_is_a_legacy_name(self):
        for name, text in self.agent_texts().items():
            for out in re.findall(r"`output/([A-Z_]+)\.md`", text):
                self.assertIn(out, LEGACY_OUTPUTS, f"{name} names unknown output {out}")

    def test_every_sub_agent_loads_at_least_one_existing_skill(self):
        for name, text in self.agent_texts().items():
            if name.startswith("sub-"):
                self.assertTrue(re.findall(r"`skills/[\w-]+/SKILL.md`", text), name)

    def test_agent_frontmatter_keeps_identity_and_baseline_model(self):
        for name, text in self.agent_texts().items():
            fm = co.yaml.safe_load(text.split("---", 2)[1])
            self.assertEqual(fm["name"], name)
            self.assertEqual(fm["model"], "sonnet")
            self.assertIn("tools", fm)

    def test_root_skill_runs_in_the_main_conversation(self):
        text = (REPO / "skills" / "hormozi-orchestrator" / "SKILL.md").read_text(encoding="utf-8")
        fm = co.yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(fm["name"], "hormozi-orchestrator")
        self.assertNotIn("context", fm)
        self.assertNotIn("agent", fm)

    def test_every_route_mode_is_documented_in_the_shared_workflow(self):
        doc = (REPO / "references" / "orchestration.md").read_text(encoding="utf-8")
        modes = {m for r in co.ROUTES.values() for pair in r["order"] for (_, m) in pair}
        modes |= {m for r in co.ROUTES.values() for (_, m) in r["required"]}
        for m in modes:
            self.assertIn(f"`{m}`", doc, f"mode {m} enforced by the checker but undocumented")


if __name__ == "__main__":
    unittest.main()
