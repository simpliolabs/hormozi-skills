"""Structured commercial identities survive generic AI blockers in controlled priced-offer runs."""

import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import build_run, read_json, sha, write_json
import check_outputs as co


POLICY = "COMMERCIAL_REFUND_CANCELLATION_UNRESOLVED"
COST = "COMMERCIAL_COST_FEASIBILITY_UNVERIFIED"


def field(value, status="approved", *, kind=None, authorization_ref="owner:terms-1", evidence=None):
    record = {"value": value, "status": status, "owner": "root", "updated": "2026-11-06T00:00:00Z"}
    if kind:
        record["kind"] = kind
    if authorization_ref is not None:
        record["authorization_ref"] = authorization_ref
    if evidence is not None:
        record["evidence"] = evidence
    return record


def money(amount=10000):
    return {"amount_minor": amount, "currency": "USD", "cadence": "monthly"}


class CommercialCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.run_dir, self.ws = build_run(self.tmp)
        self.brief = read_json(self.run_dir / "BRIEF.json")
        self.decisions = read_json(self.run_dir / "OFFER_DECISIONS.json")
        self.state = read_json(self.run_dir / "RUN_STATE.json")

    def priced(self, stage="E"):
        self.brief["stage"] = stage
        self.brief["requested_artifacts"].append("PRICING.md")

    def unknowns(self):
        fields = self.decisions["fields"]
        fields["refunds"] = field(None, "unknown", authorization_ref=None)
        fields["cancellation"] = field(None, "unknown", authorization_ref=None)
        fields["delivery_cost"] = field(None, "unknown", kind="money", authorization_ref=None)
        fields["financial_feasibility"] = field(None, "unknown", authorization_ref=None)
        fields["price_anchor"] = field("$249/month planning anchor", "proposed", authorization_ref=None)
        fields.pop("price")

    def approved(self):
        fields = self.decisions["fields"]
        fields["refunds"] = field("Refund terms approved")
        fields["cancellation"] = field("Cancellation terms approved")
        fields["delivery_cost"] = field(money(0), kind="money", evidence=["input/offer.md"])
        fields["financial_feasibility"] = field("Scoped contribution reviewed", evidence=["input/offer.md"])
        fields["price"] = field(money(24900), kind="money")
        fields["cac"] = field(money(1000), kind="money")

    def validate(self, mode="ready"):
        write_json(self.run_dir / "BRIEF.json", self.brief)
        write_json(self.run_dir / "OFFER_DECISIONS.json", self.decisions)
        self.state["decision_hash"] = co.canonical_hash(self.run_dir / "OFFER_DECISIONS.json")
        write_json(self.run_dir / "RUN_STATE.json", self.state)
        return co.validate_run(self.run_dir, self.ws, mode)

    @staticmethod
    def commercial(findings):
        return {f.code: f.reason for f in findings if f.code in (POLICY, COST)}

    def snapshot(self):
        return {p.relative_to(self.tmp).as_posix(): sha(p.read_bytes())
                for p in self.tmp.rglob("*") if p.is_file()}


class TestCommercialHoldFloor(CommercialCase):
    def test_generic_blocker_and_held_phase_cannot_hide_two_identities(self):
        self.priced()
        self.unknowns()
        self.state["phase"] = "HELD"
        self.state["blockers"] = ["Commercial terms and financial feasibility require owner approval and evidence"]
        found = self.commercial(self.validate())
        self.assertEqual(set(found), {POLICY, COST})
        self.assertIn("refund/cancellation terms unresolved", found[POLICY])
        self.assertIn("refunds=unknown", found[POLICY])
        self.assertIn("cancellation=unknown", found[POLICY])
        self.assertIn("delivery costs and financial feasibility unverified", found[COST])
        self.assertIn("delivery_cost=unknown", found[COST])
        self.assertIn("price=missing", found[COST])

    def test_missing_fields_fail_closed_and_draft_mode_does_not_add_floor(self):
        self.priced(stage="A")
        found = self.commercial(self.validate())
        self.assertEqual(set(found), {POLICY, COST})
        self.assertIn("refunds=missing", found[POLICY])
        self.assertIn("cancellation=missing", found[POLICY])
        self.assertIn("delivery_cost=missing", found[COST])
        self.assertIn("financial_feasibility=missing", found[COST])
        self.assertEqual(self.commercial(self.validate("draft")), {})

    def test_legacy_combined_policy_is_all_of_with_canonical_sources(self):
        self.priced(stage="B")
        self.approved()
        self.decisions["fields"]["refund_cancellation"] = field(None, "held", authorization_ref=None)
        found = self.commercial(self.validate())
        self.assertIn(POLICY, found)
        self.assertIn("refund_cancellation=held", found[POLICY])
        self.decisions["fields"]["refund_cancellation"] = field("Combined policy approved")
        self.assertNotIn(POLICY, self.commercial(self.validate()))

    def test_approved_terms_and_evidence_backed_costs_clear_only_new_floor(self):
        self.priced(stage="A")
        self.approved()
        self.decisions["fields"]["CAC"] = field(money(0), kind="money")
        self.assertEqual(self.commercial(self.validate()), {})

    def test_zero_is_structured_money_but_unknown_is_null(self):
        self.priced()
        self.approved()
        self.assertNotIn(COST, self.commercial(self.validate()))
        self.decisions["fields"]["delivery_cost"] = field(None, "unknown", kind="money", authorization_ref=None)
        self.assertIn("delivery_cost=unknown", self.commercial(self.validate())[COST])

    def test_proposed_terms_or_missing_authorization_do_not_clear(self):
        self.priced()
        self.approved()
        self.decisions["fields"]["refunds"] = field("Proposed refund", "proposed", authorization_ref=None)
        self.decisions["fields"]["cancellation"]["authorization_ref"] = ""
        found = self.commercial(self.validate())
        self.assertIn("refunds=proposed", found[POLICY])
        self.assertIn("cancellation=authorization_ref missing", found[POLICY])

    def test_missing_cost_evidence_or_unapproved_declared_cost_holds(self):
        self.priced()
        self.approved()
        self.decisions["fields"]["delivery_cost"].pop("evidence")
        self.decisions["fields"]["support_cost/capacity"] = field(None, "unknown", authorization_ref=None)
        found = self.commercial(self.validate())
        self.assertIn("delivery_cost=evidence missing", found[COST])
        self.assertIn("support_cost/capacity=unknown", found[COST])

    def test_focused_run_without_pricing_scope_is_lightweight(self):
        self.unknowns()
        self.brief["stage"] = "E"
        self.brief["task"] = "five hooks only"
        self.assertEqual(self.commercial(self.validate()), {})

    def test_pricing_task_triggers_at_any_stage_without_requested_file(self):
        self.unknowns()
        self.brief["stage"] = "E"
        self.state["tasks"].append({"id": "pricing", "role": "sub-pricing", "mode": "final_feasibility",
                                    "status": "done", "depends_on": [], "inputs": [], "write_set": []})
        self.assertEqual(set(self.commercial(self.validate())), {POLICY, COST})
        self.state["tasks"][-1]["status"] = "not_applicable"
        self.assertEqual(self.commercial(self.validate()), {})

    def test_pricing_manifest_path_triggers_without_request_or_task(self):
        self.unknowns()
        art = dict(self.state["artifacts"][0], path="output/PRICING.md")
        self.state["artifacts"].append(art)
        self.assertEqual(set(self.commercial(self.validate())), {POLICY, COST})

    def test_equivalent_pricing_request_spellings_trigger(self):
        self.unknowns()
        for spelling in ("PRICING.md", "output/PRICING.md", ".\\output\\PRICING.md"):
            with self.subTest(spelling=spelling):
                self.brief["requested_artifacts"] = ["PITCH.md", spelling]
                self.assertEqual(set(self.commercial(self.validate())), {POLICY, COST})

    def test_missing_decisions_or_invalid_state_still_hold_without_traceback(self):
        self.priced()
        self.validate()
        (self.run_dir / "OFFER_DECISIONS.json").unlink()
        found = co.validate_run(self.run_dir, self.ws, "ready")
        self.assertIn("CONTROL_FILE_MISSING", {f.code for f in found})
        self.assertEqual(set(self.commercial(found)), {POLICY, COST})
        write_json(self.run_dir / "OFFER_DECISIONS.json", self.decisions)
        bad_state = read_json(self.run_dir / "RUN_STATE.json")
        bad_state.pop("phase")
        write_json(self.run_dir / "RUN_STATE.json", bad_state)
        found = co.validate_run(self.run_dir, self.ws, "ready")
        self.assertIn("SCHEMA_INVALID", {f.code for f in found})
        self.assertEqual(set(self.commercial(found)), {POLICY, COST})

    def test_numeric_policy_and_superseded_alias_cannot_clear(self):
        self.priced()
        self.approved()
        self.decisions["fields"]["refunds"]["value"] = 0
        self.assertIn("refunds=policy text missing", self.commercial(self.validate())[POLICY])
        self.decisions["fields"]["refunds"]["value"] = "Refund policy approved"
        self.decisions["fields"]["refund_policy"] = field("Old policy", "superseded")
        self.assertIn("refund_policy=superseded", self.commercial(self.validate())[POLICY])

    def test_fulfillment_cost_alias_must_resolve_with_delivery_cost(self):
        self.priced()
        self.approved()
        self.decisions["fields"]["fulfillment_cost"] = field(None, "unknown", kind="money",
                                                            authorization_ref=None)
        self.assertIn("fulfillment_cost=unknown", self.commercial(self.validate())[COST])

    def test_checker_is_read_only(self):
        self.priced()
        self.unknowns()
        self.validate()
        before = self.snapshot()
        co.validate_run(self.run_dir, self.ws, "ready")
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
