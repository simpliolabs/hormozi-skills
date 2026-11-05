"""Independent-review floor: sales output, canonical copy files and explicit high_risk need a separate-context pass.

Everything goes through the public validate_run / CLI. Author flags (high_risk false/absent, ready=false, phase HELD)
cannot waive the floor in ready validation, and one aggregate blocker is surfaced while any obligation is open.
"""
import contextlib
import hashlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import build_run, codes, read_json, write_json, sha
import check_outputs as co

BLOCKER = "[review] Independent review remains required."
HR = "HIGH_RISK_NO_INDEPENDENT_REVIEW"


def of(findings, code, reason=None):
    return [f for f in findings if f.code == code and (reason is None or BLOCKER in f.reason)]


class FloorCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.run_dir, self.ws = build_run(self.tmp)

    def validate(self, mode="ready"):
        return co.validate_run(self.run_dir, self.ws, mode)

    def edit(self, fn):
        st = read_json(self.run_dir / "RUN_STATE.json")
        fn(st)
        write_json(self.run_dir / "RUN_STATE.json", st)

    def make_same_context(self):
        self.edit(lambda s: s["reviews"][0].update(context="same", reviewer="root"))

    def add_file_artifact(self, rel, *, role="root", task_id=None, high_risk=None, context="same", spelling=None, text="# Notes\n\nPlain notes.\n"):
        """Add one manifested file (written at rel, listed as spelling) with a passing review of the given context."""
        out = self.ws / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        h, shown, tid = sha(out.read_bytes()), spelling or rel, task_id or f"t_{abs(hash(rel))}"

        def f(st):
            st["tasks"].append({"id": tid, "role": role, "status": "done", "depends_on": [], "inputs": [], "write_set": [shown]})
            art = {"path": shown, "sha256": h, "decision_version": 3, "task": tid, "ready": True}
            if high_risk is not None:
                art["high_risk"] = high_risk
            st["artifacts"].append(art)
            st["reviews"].append({"artifact": shown, "artifact_sha256": h, "decision_version": 3,
                                  "reviewer": "adversary" if context == "separate" else "root", "context": context, "result": "pass"})
        self.edit(f)
        return shown


class TestFloorOnSalesOutput(FloorCase):
    def test_separate_pass_satisfies_obligation(self):
        self.assertEqual(self.validate(), [])

    def test_false_flag_same_context_is_held_with_aggregate_blocker(self):
        self.make_same_context()
        self.edit(lambda s: s["artifacts"][0].__setitem__("high_risk", False))
        got = self.validate()
        self.assertEqual(len(of(got, HR)), 1)
        self.assertEqual(of(got, HR)[0].artifact, "output/PITCH.md")
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_absent_flag_same_context_is_held_with_aggregate_blocker(self):
        self.make_same_context()
        self.assertNotIn("high_risk", read_json(self.run_dir / "RUN_STATE.json")["artifacts"][0])
        got = self.validate()
        self.assertEqual(len(of(got, HR)), 1)
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_no_review_keeps_generic_and_specific_findings(self):
        self.edit(lambda s: s.__setitem__("reviews", []))
        got = self.validate()
        self.assertTrue(of(got, "REVIEW_STALE_OR_MISSING"))
        self.assertEqual(len(of(got, HR)), 1)
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_failed_review_keeps_both_findings(self):
        self.edit(lambda s: s["reviews"][0].update(result="fail"))
        got = self.validate()
        self.assertTrue(of(got, "REVIEW_STALE_OR_MISSING"))
        self.assertEqual(len(of(got, HR)), 1)

    def test_stale_hash_review_keeps_both_findings(self):
        self.edit(lambda s: s["reviews"][0].update(artifact_sha256="0" * 64))
        got = self.validate()
        self.assertTrue(of(got, "REVIEW_STALE_OR_MISSING"))
        self.assertEqual(len(of(got, HR)), 1)

    def test_stale_decision_version_review_keeps_both_findings(self):
        self.edit(lambda s: s["reviews"][0].update(decision_version=2))
        got = self.validate()
        self.assertTrue(of(got, "REVIEW_STALE_OR_MISSING"))
        self.assertEqual(len(of(got, HR)), 1)

    def test_separate_pass_for_other_artifact_does_not_count(self):
        self.make_same_context()
        self.add_file_artifact("output/NOTES.md", context="separate")
        got = self.validate()
        self.assertEqual([f.artifact for f in of(got, HR)], ["output/PITCH.md"])

    def test_same_context_pass_plus_separate_pass_for_same_artifact_satisfies(self):
        def f(st):
            st["reviews"][0].update(context="same", reviewer="root")
            r = dict(st["reviews"][0], context="separate", reviewer="adversary")
            st["reviews"].append(r)
        self.edit(f)
        self.assertEqual(self.validate(), [])

    def test_held_phase_and_ready_false_cannot_bypass(self):
        self.make_same_context()

        def f(st):
            st["phase"] = "HELD"
            st["artifacts"][0]["ready"] = False
        self.edit(f)
        got = self.validate("ready")
        self.assertEqual(len(of(got, HR)), 1)
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_draft_behaviour_is_unchanged(self):
        self.make_same_context()
        got = self.validate("draft")
        self.assertFalse(of(got, HR))
        self.assertFalse(of(got, "BLOCKER_OPEN"))

    def test_no_business_blocker_negative_still_fails_readiness(self):
        self.make_same_context()
        self.assertEqual(read_json(self.run_dir / "RUN_STATE.json")["blockers"], [])
        self.assertTrue([f for f in self.validate() if f.severity == "error"])


class TestRoleAndPathIdentity(FloorCase):
    def test_renamed_and_bookkeeping_like_sales_outputs_are_covered(self):
        names = ["output/renamed_offer_copy.md", "output/review.md", "output/QA_REPORT.md", "output/CHECKPOINT.md",
                 "output/runs/run1/receipt.md", "output/notes.txt"]
        for name in names:
            with self.subTest(name=name):
                self.setUp()
                self.add_file_artifact(name, role="sub-sales", context="same", high_risk=False)
                got = self.validate()
                self.assertIn(name, [f.artifact for f in of(got, HR)])
                self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_canonical_files_owned_by_root_are_covered(self):
        for name in ("output/PITCH.md", "output/HOOKS.md", "output/LANDING_PAGE.md"):
            with self.subTest(name=name):
                self.setUp()
                if name == "output/PITCH.md":
                    def f(st):
                        st["tasks"].append({"id": "t_root", "role": "root", "status": "done", "depends_on": [], "inputs": [], "write_set": [name]})
                        st["artifacts"][0]["task"] = "t_root"
                        st["reviews"][0].update(context="same", reviewer="root")
                    self.edit(f)
                else:
                    self.add_file_artifact(name, role="root", context="same")
                got = self.validate()
                self.assertIn(name, [f.artifact for f in of(got, HR)])
                self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_safe_equivalent_spellings_of_canonical_files_are_covered(self):
        for spelling in ("./output/HOOKS.md", "output\\HOOKS.md", "output/sub/../HOOKS.md"):
            with self.subTest(spelling=spelling):
                self.setUp()
                self.add_file_artifact("output/HOOKS.md", role="root", context="same", spelling=spelling)
                got = self.validate()
                self.assertIn(spelling, [f.artifact for f in of(got, HR)])

    def test_canonical_file_with_separate_pass_is_accepted(self):
        self.add_file_artifact("output/LANDING_PAGE.md", role="root", context="separate")
        self.assertEqual(self.validate(), [])

    def test_unrelated_low_risk_non_sales_output_needs_no_independent_review(self):
        self.add_file_artifact("output/NOTES.md", role="root", context="same")
        self.add_file_artifact("output/RESEARCH.md", role="sub-market", context="same", high_risk=False)
        got = self.validate()
        self.assertFalse(of(got, HR))
        self.assertFalse(of(got, "BLOCKER_OPEN"))

    def test_explicit_high_risk_non_sales_keeps_requirement(self):
        self.add_file_artifact("output/NOTES.md", role="root", context="same", high_risk=True)
        got = self.validate()
        self.assertEqual([f.artifact for f in of(got, HR)], ["output/NOTES.md"])
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_explicit_high_risk_non_sales_with_separate_pass_is_accepted(self):
        self.add_file_artifact("output/NOTES.md", role="root", context="separate", high_risk=True)
        self.assertEqual(self.validate(), [])


class TestMissingFileKeepsObligations(FloorCase):
    def test_missing_file_still_reports_review_holds_in_every_arm(self):
        arms = {"role-only renamed sales": dict(rel="output/renamed_copy.md", role="sub-sales"),
                "canonical root-owned": dict(rel="output/HOOKS.md", role="root"),
                "explicit high-risk non-sales": dict(rel="output/NOTES.md", role="root", high_risk=True)}
        for name, kw in arms.items():
            for variant in ("same-context", "no-review"):
                with self.subTest(arm=name, variant=variant):
                    self.setUp()
                    rel = kw["rel"]
                    self.add_file_artifact(rel, role=kw["role"], high_risk=kw.get("high_risk"), context="same")
                    (self.ws / rel).unlink()

                    def f(st):
                        st["phase"] = "HELD"
                        st["artifacts"][-1]["ready"] = False
                        if variant == "no-review":
                            st["reviews"] = [r for r in st["reviews"] if r["artifact"] != rel]
                    self.edit(f)
                    got = self.validate()
                    self.assertTrue([f for f in got if f.code == "ARTIFACT_MISSING" and f.artifact == rel])
                    self.assertEqual([f.artifact for f in of(got, HR)], [rel])
                    self.assertEqual(bool(of(got, "REVIEW_STALE_OR_MISSING")), variant == "no-review")
                    self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_missing_file_draft_mode_unchanged(self):
        self.add_file_artifact("output/renamed_copy.md", role="sub-sales", context="same")
        (self.ws / "output/renamed_copy.md").unlink()
        self.assertFalse(of(self.validate("draft"), HR))


class TestAggregateBlocker(FloorCase):
    def three_sales_same_context(self):
        self.make_same_context()
        self.add_file_artifact("output/HOOKS.md", role="sub-sales", context="same")
        self.add_file_artifact("output/LANDING_PAGE.md", role="sub-sales", context="same")

    def test_three_business_blockers_plus_one_aggregate_plus_three_holds(self):
        self.three_sales_same_context()
        self.edit(lambda s: s.__setitem__("blockers", ["[price] not approved", "[guarantee] not approved", "[claim] unverified"]))
        got = self.validate()
        self.assertEqual(len(of(got, HR)), 3)
        self.assertEqual({f.artifact for f in of(got, HR)}, {"output/PITCH.md", "output/HOOKS.md", "output/LANDING_PAGE.md"})
        blockers = of(got, "BLOCKER_OPEN")
        self.assertEqual(len(blockers), 4)
        for b in ("[price] not approved", "[guarantee] not approved", "[claim] unverified"):
            self.assertEqual(len([f for f in blockers if f.reason.endswith(b)]), 1)
        self.assertEqual(len(of(blockers, "BLOCKER_OPEN", BLOCKER)), 1)
        self.assertEqual(len(blockers) + len(of(got, HR)), 7)

    def test_explicit_sentinel_is_reused_not_duplicated(self):
        self.three_sales_same_context()
        self.edit(lambda s: s.__setitem__("blockers", [BLOCKER]))
        got = self.validate()
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)
        self.assertEqual(len(of(got, "BLOCKER_OPEN")), 1)

    def test_sentinel_with_unrelated_blocker_keeps_both(self):
        self.make_same_context()
        self.edit(lambda s: s.__setitem__("blockers", ["[price] not approved", BLOCKER]))
        got = self.validate()
        self.assertEqual(len(of(got, "BLOCKER_OPEN")), 2)

    def test_stale_explicit_sentinel_is_not_cleared_by_checker(self):
        self.edit(lambda s: s.__setitem__("blockers", [BLOCKER]))
        got = self.validate()
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)
        self.assertFalse(of(got, HR))

    def test_unrelated_blocker_prose_is_not_treated_as_the_sentinel(self):
        self.make_same_context()
        self.edit(lambda s: s.__setitem__("blockers", ["independent review remains required (approved by owner)"]))
        got = self.validate()
        self.assertEqual(len(of(got, "BLOCKER_OPEN")), 2)
        self.assertEqual(len(of(got, "BLOCKER_OPEN", BLOCKER)), 1)

    def test_no_aggregate_when_every_obligation_is_satisfied(self):
        self.assertFalse(of(self.validate(), "BLOCKER_OPEN"))


class TestReadOnlyAndCli(FloorCase):
    def snapshot(self):
        return {str(p.relative_to(self.tmp)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(self.tmp.rglob("*")) if p.is_file()}

    def test_checker_leaves_every_input_byte_identical(self):
        self.make_same_context()
        before = self.snapshot()
        self.validate()
        self.validate("draft")
        self.assertEqual(before, self.snapshot())

    def test_cli_reports_specific_and_aggregate_findings_and_exits_held(self):
        self.make_same_context()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = co.main(["--run", str(self.run_dir), "--workspace", str(self.ws), "--json"])
        self.assertEqual(rc, co.EXIT_HELD)
        data = json.loads(buf.getvalue())
        self.assertEqual(len([d for d in data if d["code"] == HR]), 1)
        self.assertEqual(len([d for d in data if d["code"] == "BLOCKER_OPEN" and BLOCKER in d["reason"]]), 1)

    def test_cli_passes_with_separate_review(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = co.main(["--run", str(self.run_dir), "--workspace", str(self.ws)])
        self.assertEqual(rc, co.EXIT_PASS)


if __name__ == "__main__":
    unittest.main()
