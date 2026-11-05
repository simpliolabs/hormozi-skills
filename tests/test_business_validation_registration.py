"""Declared business-validation limitation must be registered in RUN_STATE.blockers.

Root declares the known limitation as the exact string in BRIEF.constraints; ready validation then requires the identical
blocker. Everything goes through the public validate_run. The checker never infers the limitation from source types,
facts, prose or identity, never writes, and never clears an explicit blocker.
"""
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import build_run, codes, read_json, write_json, sha
import check_outputs as co

MARKER = "Fictional fixture; real business validation absent"
UNREG = "BUSINESS_VALIDATION_BLOCKER_UNREGISTERED"
REVIEW_BLOCKER = "[review] Independent review remains required."


def hold(findings, text=MARKER):
    return [f for f in findings if f.code == "BLOCKER_OPEN" and f.reason == f"unresolved blocker: {text}"]


class RegistrationCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.run_dir, self.ws = build_run(self.tmp)

    def validate(self, mode="ready"):
        return co.validate_run(self.run_dir, self.ws, mode)

    def edit(self, name, fn):
        doc = read_json(self.run_dir / name)
        fn(doc)
        write_json(self.run_dir / name, doc)

    def declare(self, text=MARKER):
        self.edit("BRIEF.json", lambda b: b["constraints"].append(text))

    def register(self, text=MARKER):
        self.edit("RUN_STATE.json", lambda s: s["blockers"].append(text))

    def snapshot(self):
        return {p: sha(p.read_bytes()) for p in self.tmp.rglob("*") if p.is_file()}


class TestMissingRegistration(RegistrationCase):
    def test_baseline_without_marker_is_clean(self):
        self.assertEqual(self.validate(), [])

    def test_marker_without_blocker_derives_one_hold_and_error(self):
        self.declare()
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertEqual([f.code for f in got if f.code == UNREG], [UNREG])
        self.assertEqual(codes(got), {"BLOCKER_OPEN", UNREG})
        self.assertTrue(all(f.severity == "error" for f in got))

    def test_exact_state_blocker_reuses_ordinary_finding(self):
        self.declare()
        self.register()
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertNotIn(UNREG, codes(got))

    def test_state_blocker_without_marker_is_ordinary_only(self):
        self.register()
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertNotIn(UNREG, codes(got))

    def test_held_phase_cannot_waive(self):
        self.declare()
        self.edit("RUN_STATE.json", lambda s: s.update(phase="HELD"))
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertIn(UNREG, codes(got))

    def test_artifact_ready_false_cannot_waive(self):
        self.declare()
        self.edit("RUN_STATE.json", lambda s: s["artifacts"][0].update(ready=False))
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertIn(UNREG, codes(got))

    def test_unrelated_blockers_do_not_substitute(self):
        self.declare()
        self.register("[timing] Launch date unconfirmed.")
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertIn(UNREG, codes(got))
        self.assertEqual(len(hold(got, "[timing] Launch date unconfirmed.")), 1)

    def test_review_blocker_does_not_substitute(self):
        self.declare()
        self.register(REVIEW_BLOCKER)
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertIn(UNREG, codes(got))

    def test_unrelated_finding_does_not_waive(self):
        self.declare()
        self.edit("RUN_STATE.json", lambda s: s["tasks"][1].update(status="running"))
        got = self.validate()
        self.assertIn("TASK_INCOMPLETE_IN_READY", codes(got))
        self.assertEqual(len(hold(got)), 1)
        self.assertIn(UNREG, codes(got))


class TestIndependentReviewInteraction(RegistrationCase):
    def test_valid_separate_review_leaves_business_hold(self):
        self.declare()
        got = self.validate()
        self.assertNotIn("HIGH_RISK_NO_INDEPENDENT_REVIEW", codes(got))
        self.assertNotIn("REVIEW_STALE_OR_MISSING", codes(got))
        self.assertEqual(len(hold(got)), 1)
        self.assertEqual(len(hold(got, REVIEW_BLOCKER)), 0)

    def test_missing_separate_review_adds_review_hold_beside_business_hold(self):
        self.declare()
        self.edit("RUN_STATE.json", lambda s: s["reviews"][0].update(context="same", reviewer="root"))
        got = self.validate()
        self.assertIn("HIGH_RISK_NO_INDEPENDENT_REVIEW", codes(got))
        self.assertEqual(len(hold(got, REVIEW_BLOCKER)), 1)
        self.assertEqual(len(hold(got)), 1)
        self.assertIn(UNREG, codes(got))


class TestMarkerIsExact(RegistrationCase):
    NEAR = [
        MARKER + ".",
        MARKER.lower(),
        "Fictional fixture, real business validation absent",
        "Fictional fixture; real validation absent",
        MARKER + " (see notes)",
        " " + MARKER,
        "Note: " + MARKER,
    ]

    def test_near_matches_in_constraints_derive_nothing(self):
        for text in self.NEAR:
            with self.subTest(text=text):
                self.edit("BRIEF.json", lambda b, t=text: b.update(constraints=[t]))
                self.assertEqual(self.validate(), [])

    def test_near_match_state_blocker_does_not_register(self):
        self.declare()
        self.register(MARKER + ".")
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertEqual(len(hold(got, MARKER + ".")), 1)
        self.assertIn(UNREG, codes(got))

    def test_marker_among_other_constraints_triggers(self):
        self.edit("BRIEF.json", lambda b: b.update(constraints=["Keep it short", MARKER, "No jargon"]))
        self.assertIn(UNREG, codes(self.validate()))

    def test_narrative_disclaimer_elsewhere_derives_nothing(self):
        self.edit("BRIEF.json", lambda b: b.update(unknowns=[MARKER], goal=MARKER))
        self.assertEqual(self.validate(), [])


class TestNoInferenceFromProvenance(RegistrationCase):
    def test_synthetic_only_without_marker_derives_nothing(self):
        self.edit("BRIEF.json", lambda b: b.update(
            facts=[{"id": "f1", "text": "Fictional customer data", "source_type": "synthetic"}]))
        self.assertEqual(self.validate(), [])
        self.assertEqual(self.validate("draft"), [])

    def test_fictional_wording_without_marker_derives_nothing(self):
        self.edit("BRIEF.json", lambda b: b.update(
            customer="Fictional coaches",
            facts=[{"id": "f1", "text": "Fictional fixture", "source_type": "synthetic"}]))
        self.assertEqual(self.validate(), [])

    def test_supplied_facts_with_marker_triggers(self):
        self.declare()
        self.assertEqual(read_json(self.run_dir / "BRIEF.json")["facts"][0]["source_type"], "supplied")
        self.assertIn(UNREG, codes(self.validate()))

    def test_mixed_facts_with_marker_triggers(self):
        self.declare()
        self.edit("BRIEF.json", lambda b: b["facts"].append(
            {"id": "f2", "text": "illustrative", "source_type": "synthetic"}))
        got = self.validate()
        self.assertEqual(len(hold(got)), 1)
        self.assertIn(UNREG, codes(got))

    def test_synthetic_only_with_marker_triggers(self):
        self.declare()
        self.edit("BRIEF.json", lambda b: b.update(
            facts=[{"id": "f1", "text": "Fictional customer data", "source_type": "synthetic"}]))
        self.assertIn(UNREG, codes(self.validate()))


class TestInvalidAndMissingControls(RegistrationCase):
    def test_invalid_brief_derives_nothing_and_keeps_schema_error(self):
        self.declare()
        self.edit("BRIEF.json", lambda b: b.pop("goal"))
        got = self.validate()
        self.assertIn("SCHEMA_INVALID", codes(got))
        self.assertNotIn(UNREG, codes(got))
        self.assertEqual(hold(got), [])

    def test_missing_brief_derives_nothing(self):
        self.declare()
        (self.run_dir / "BRIEF.json").unlink()
        got = self.validate()
        self.assertIn("CONTROL_FILE_MISSING", codes(got))
        self.assertNotIn(UNREG, codes(got))
        self.assertEqual(hold(got), [])

    def test_malformed_brief_json_does_not_crash(self):
        (self.run_dir / "BRIEF.json").write_text("{not json", encoding="utf-8")
        got = self.validate()
        self.assertIn("SCHEMA_INVALID", codes(got))
        self.assertNotIn(UNREG, codes(got))

    def test_non_list_constraints_is_schema_invalid_not_a_crash(self):
        self.edit("BRIEF.json", lambda b: b.update(constraints=MARKER))
        got = self.validate()
        self.assertIn("SCHEMA_INVALID", codes(got))
        self.assertNotIn(UNREG, codes(got))

    def test_invalid_state_derives_nothing(self):
        self.declare()
        self.edit("RUN_STATE.json", lambda s: s.pop("blockers"))
        got = self.validate()
        self.assertIn("SCHEMA_INVALID", codes(got))
        self.assertNotIn(UNREG, codes(got))
        self.assertEqual(hold(got), [])

    def test_missing_state_derives_nothing(self):
        self.declare()
        (self.run_dir / "RUN_STATE.json").unlink()
        got = self.validate()
        self.assertIn("CONTROL_FILE_MISSING", codes(got))
        self.assertNotIn(UNREG, codes(got))


class TestDraftAndReadOnly(RegistrationCase):
    def test_draft_mode_unchanged(self):
        self.assertEqual(self.validate("draft"), [])
        self.declare()
        self.assertEqual(self.validate("draft"), [])

    def test_draft_with_registered_blocker_stays_draft_clean(self):
        self.declare()
        self.register()
        self.assertEqual(self.validate("draft"), [])

    def test_validation_is_read_only_and_never_clears(self):
        self.declare()
        self.register()
        before = self.snapshot()
        for mode in ("ready", "draft"):
            self.validate(mode)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(read_json(self.run_dir / "RUN_STATE.json")["blockers"], [MARKER])

    def test_missing_registration_leaves_inputs_byte_identical(self):
        self.declare()
        before = self.snapshot()
        self.validate()
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(read_json(self.run_dir / "RUN_STATE.json")["blockers"], [])


if __name__ == "__main__":
    unittest.main()
