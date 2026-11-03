"""Task 4 acceptance gaps: canonical money, ready blockers, producer completion, identity, exact paths."""
import unittest

from helpers import codes, read_json, write_json, refresh_artifact_hash
from test_outputs import RunCase


class MoneyCase(RunCase):
    def render(self, old, new, drop_display=True):
        p = self.ws / "output" / "PITCH.md"
        p.write_text(p.read_text().replace(old, new))
        refresh_artifact_hash(self.run_dir, self.ws)
        self.edit_state(lambda s: s["artifacts"][0]["bindings"][0].__setitem__("rendered_text", new))
        if drop_display:
            self.edit_decisions(lambda d: d["fields"]["price"].pop("display"))


class TestCanonicalMoney(MoneyCase):
    def test_probe_wrong_price_without_display_is_held(self):
        # ROOT_CANONICAL_PRICE_PROBE: canonical USD 250 yearly vs rendered USD 999 monthly, display omitted
        self.edit_decisions(lambda d: d["fields"]["price"].update(
            value={"amount_minor": 25000, "currency": "USD", "cadence": "yearly"}))
        self.render("$2,500 one-time", "USD 999 monthly")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_correct_rendering_without_display_passes(self):
        self.render("$2,500 one-time", "$2,500 one-time")
        self.assertEqual(self.validate(), [])

    def test_code_prefixed_rendering_passes(self):
        self.render("$2,500 one-time", "USD 2,500 one-time")
        self.assertEqual(self.validate(), [])

    def test_wrong_amount_held(self):
        self.render("$2,500 one-time", "$2,000 one-time")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_wrong_cadence_held(self):
        self.render("$2,500 one-time", "$2,500 per month")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_wrong_currency_held(self):
        self.render("$2,500 one-time", "EUR 2,500 one-time")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_missing_cadence_held(self):
        self.render("$2,500 one-time", "$2,500")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_display_contradicting_value_held(self):
        # display and binding agree with each other but contradict the structured value
        self.render("$2,500 one-time", "$999 monthly", drop_display=False)
        self.edit_decisions(lambda d: d["fields"]["price"].update(display="$999 monthly"))
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_unrelated_example_amount_in_prose_still_allowed(self):
        p = self.ws / "output" / "PITCH.md"
        p.write_text(p.read_text() + "\nExample: one $10,000 contract per year recoups the fee.\n")
        refresh_artifact_hash(self.run_dir, self.ws)
        self.assertEqual(self.validate(), [])

    def test_money_shaped_value_requires_money_kind(self):
        self.edit_decisions(lambda d: d["fields"]["price"].pop("kind"))
        self.assertIn("SCHEMA_INVALID", codes(self.validate()))


class TestGuaranteeConditions(RunCase):
    def test_condition_missing_from_rendered_terms_held(self):
        short = "Refund within 30 days"
        p = self.ws / "output" / "PITCH.md"
        p.write_text(p.read_text().replace("Refund within 30 days if you complete every module and show no result", short))
        refresh_artifact_hash(self.run_dir, self.ws)
        self.edit_state(lambda s: s["artifacts"][0]["bindings"][1].__setitem__("rendered_text", short))
        self.edit_decisions(lambda d: d["fields"]["guarantee"].update(display=short))
        self.assertIn("GUARANTEE_CONDITION_MISSING", codes(self.validate()))


class TestReadyGates(RunCase):
    def test_unresolved_blocker_holds_ready(self):
        self.edit_state(lambda s: s.__setitem__("blockers", ["pricing input unknown"]))
        self.assertIn("BLOCKER_OPEN", codes(self.validate("ready")))
        self.assertNotIn("BLOCKER_OPEN", codes(self.validate("draft")))

    def test_producer_task_not_done_holds_ready(self):
        self.edit_state(lambda s: s["tasks"][1].__setitem__("status", "failed"))
        self.assertIn("ARTIFACT_PRODUCER_INCOMPLETE", codes(self.validate("ready")))

    def test_required_task_unfinished_holds_ready(self):
        self.edit_state(lambda s: s["tasks"][0].__setitem__("status", "pending"))
        self.assertIn("TASK_INCOMPLETE_IN_READY", codes(self.validate("ready")))
        self.assertNotIn("TASK_INCOMPLETE_IN_READY", codes(self.validate("draft")))


class TestIdentity(RunCase):
    def test_run_id_mismatch(self):
        self.edit_state(lambda s: s.__setitem__("run_id", "other"))
        self.assertIn("RUN_IDENTITY_MISMATCH", codes(self.validate()))

    def test_offer_id_mismatch_between_brief_and_decisions(self):
        self.edit_decisions(lambda d: d.__setitem__("offer_id", "offer2"))
        self.assertIn("RUN_IDENTITY_MISMATCH", codes(self.validate()))


class TestExactRequestedPaths(RunCase):
    def test_same_basename_in_other_directory_does_not_satisfy(self):
        b = read_json(self.run_dir / "BRIEF.json")
        b["requested_artifacts"] = ["drafts/PITCH.md"]
        write_json(self.run_dir / "BRIEF.json", b)
        self.assertIn("REQUESTED_ARTIFACT_MISSING", codes(self.validate()))

    def test_output_prefixed_request_matches_exactly(self):
        b = read_json(self.run_dir / "BRIEF.json")
        b["requested_artifacts"] = ["output/PITCH.md"]
        write_json(self.run_dir / "BRIEF.json", b)
        self.assertEqual(self.validate(), [])


if __name__ == "__main__":
    unittest.main()
