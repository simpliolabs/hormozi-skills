"""Checker review fixes: duplicate ids, currency minor units, negative monetary renderings.

SIMULATED records in a temp workspace; the gate is asserted over actual bytes. Not native-run evidence.
Markdown bullet vs numeric minus: a bare ASCII hyphen + blanks that opens a line is a list bullet and is accepted;
every other sign (attached, Unicode minus/dashes, spaced mid-line) is held as negative-or-ambiguous.
"""
import unittest

from helpers import codes, write_json, refresh_artifact_hash, read_json
from test_acceptance_gaps import MoneyCase
from test_outputs import RunCase

BLOCKED = "We report payments to every credit bureau every month"


def claim(cid, wording, status):
    return {"id": cid, "wording": wording, "source_type": "supplied", "status": status, "sources": ["input/offer.md"],
            "scope": "pitch", "qualifications": [], "checked_at": "2026-11-03T00:00:00Z", "owner": "root"}


class TestDuplicateIds(RunCase):
    def add_pitch_wording(self):
        p = self.ws / "output" / "PITCH.md"
        p.write_text(p.read_text() + f"\n{BLOCKED}.\n")
        refresh_artifact_hash(self.run_dir, self.ws)

    def claims(self, fn):
        c = read_json(self.run_dir / "CLAIMS.json")
        fn(c)
        write_json(self.run_dir / "CLAIMS.json", c)

    def test_duplicate_claim_id_unsupported_before_verified_held(self):
        self.add_pitch_wording()
        self.claims(lambda c: c["claims"].insert(0, claim("c1", BLOCKED, "unsupported")))
        self.assertIn("CLAIM_ID_DUPLICATE", codes(self.validate()))

    def test_duplicate_claim_id_unsupported_after_verified_held(self):
        self.add_pitch_wording()
        self.claims(lambda c: c["claims"].append(claim("c1", BLOCKED, "unsupported")))
        self.assertIn("CLAIM_ID_DUPLICATE", codes(self.validate()))

    def test_distinct_claim_ids_pass(self):
        self.claims(lambda c: c["claims"].append(claim("c2", "A second supported statement", "verified")))
        self.assertEqual(self.validate(), [])

    def test_duplicate_task_id_with_other_role_held(self):
        def dup(s):
            t = dict(s["tasks"][1])
            t["role"] = "root"
            s["tasks"].append(t)
        self.edit_state(dup)
        self.assertIn("TASK_ID_DUPLICATE", codes(self.validate()))

    def test_duplicate_binding_field_with_contradictory_rendering_held(self):
        self.edit_state(lambda s: s["artifacts"][0]["bindings"].append({"field": "price", "rendered_text": "$999 one-time"}))
        self.assertIn("BINDING_FIELD_DUPLICATE", codes(self.validate()))


class Utf8Money(MoneyCase):
    """Same as MoneyCase.render but UTF-8 and LF-exact, so non-ASCII signs and newlines reach the checker as written."""

    def render(self, old, new, drop_display=True):
        p = self.ws / "output" / "PITCH.md"
        p.write_bytes(p.read_bytes().decode("utf-8").replace(old, new).encode("utf-8"))
        refresh_artifact_hash(self.run_dir, self.ws)
        self.edit_state(lambda s: s["artifacts"][0]["bindings"][0].__setitem__("rendered_text", new))
        if drop_display:
            self.edit_decisions(lambda d: d["fields"]["price"].pop("display", None))


class TestCurrencyExponent(Utf8Money):
    def jpy(self, amount_minor=2500, currency="JPY"):
        self.edit_decisions(lambda d: d["fields"]["price"]["value"].update(amount_minor=amount_minor, currency=currency))

    def test_jpy_zero_exponent_renders_whole_yen(self):
        self.jpy()
        self.render("$2,500 one-time", "JPY 2,500 one-time")
        self.assertEqual(self.validate(), [])

    def test_jpy_divided_by_100_rendering_held(self):
        self.jpy()
        self.render("$2,500 one-time", "JPY 25 one-time")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_unsupported_exponent_currency_fails_closed(self):
        self.jpy(currency="KWD")  # three-decimal currency, not in the table
        self.render("$2,500 one-time", "KWD 2.500 one-time")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_usd_and_eur_unchanged(self):
        self.render("$2,500 one-time", "$2,500 one-time")
        self.assertEqual(self.validate(), [])
        self.edit_decisions(lambda d: d["fields"]["price"]["value"].update(currency="EUR"))
        self.render("$2,500 one-time", "€2,500 one-time", drop_display=False)
        self.assertEqual(self.validate(), [])


class TestNegativeRenderings(Utf8Money):
    def test_signed_variants_held(self):
        for text in ("-$2,500 one-time", "−$2,500 one-time", "$-2,500 one-time", "$−2,500 one-time",
                     "-USD 2,500 one-time", "USD -2,500 one-time", "USD−2,500 one-time", "-2,500 USD one-time",
                     "€-2,500 one-time", "$2,500 one-time -$2,500", "Price - $2,500 one-time",
                     "− $2,500 one-time", "$2,500 one-time, USD 2,500 USD -9,999"):
            with self.subTest(text=text):
                self.render("$2,500 one-time", text)
                self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))
                self.render(text, "$2,500 one-time", drop_display=False)

    def test_markdown_bullet_is_a_list_not_a_negative(self):
        for text in ("- $2,500 one-time", "  - USD 2,500 one-time", "> - $2,500 one-time", "intro\n- $2,500 one-time"):
            with self.subTest(text=text):
                self.render("$2,500 one-time", text)
                self.assertEqual(self.validate(), [])
                self.render(text, "$2,500 one-time", drop_display=False)

    def test_bullet_does_not_swallow_a_second_wrong_amount(self):
        self.render("$2,500 one-time", "- $2,500 one-time\n- $9,999")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))

    def test_bullet_then_attached_minus_held(self):
        self.render("$2,500 one-time", "- -$2,500 one-time")
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.validate()))


if __name__ == "__main__":
    unittest.main()
