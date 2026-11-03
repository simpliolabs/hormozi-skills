import copy
import json
import unittest

import helpers  # noqa: F401  (sets sys.path)
from jsonschema import Draft202012Validator
import check_outputs as co


def schema(name):
    return json.loads((helpers.REPO / "contracts" / f"{name}.schema.json").read_text(encoding="utf-8"))


def errors(name, doc):
    return list(Draft202012Validator(schema(name)).iter_errors(doc))


GOOD_DECISIONS = {
    "schema_version": 1, "offer_id": "o", "version": 1, "parent_hash": None,
    "fields": {
        "price": {"kind": "money", "value": {"amount_minor": 250000, "currency": "USD", "cadence": "yearly"},
                  "status": "proposed", "owner": "root", "updated": "2026-11-03T00:00:00Z"},
        "fulfillment_cost": {"kind": "money", "value": None, "status": "unknown", "owner": "root", "updated": "x"},
    },
}


class TestSchemasAreValid(unittest.TestCase):
    def test_four_schemas_are_valid_2020_12(self):
        names = ["brief", "offer-decisions", "claims", "run-state"]
        for n in names:
            Draft202012Validator.check_schema(schema(n))
        self.assertEqual(len(names), 4)

    def test_good_decisions_pass(self):
        self.assertEqual(errors("offer-decisions", GOOD_DECISIONS), [])


class TestDecisionNegatives(unittest.TestCase):
    def mutate(self, fn):
        d = copy.deepcopy(GOOD_DECISIONS)
        fn(d)
        return errors("offer-decisions", d)

    def test_unknown_is_never_zero(self):
        self.assertTrue(self.mutate(lambda d: d["fields"]["fulfillment_cost"].update(value=0)))
        self.assertTrue(self.mutate(lambda d: d["fields"]["fulfillment_cost"].update(value={"amount_minor": 0, "currency": "USD", "cadence": "one_time"})))

    def test_float_money_rejected(self):
        self.assertTrue(self.mutate(lambda d: d["fields"]["price"]["value"].update(amount_minor=2500.5)))

    def test_negative_money_rejected(self):
        self.assertTrue(self.mutate(lambda d: d["fields"]["price"]["value"].update(amount_minor=-1)))

    def test_money_requires_currency_and_cadence(self):
        self.assertTrue(self.mutate(lambda d: d["fields"]["price"]["value"].pop("currency")))
        self.assertTrue(self.mutate(lambda d: d["fields"]["price"]["value"].pop("cadence")))

    def test_bad_status_rejected(self):
        self.assertTrue(self.mutate(lambda d: d["fields"]["price"].update(status="maybe")))

    def test_unknown_extra_field_rejected(self):
        self.assertTrue(self.mutate(lambda d: d.update(surprise=1)))

    def test_parent_hash_format(self):
        self.assertTrue(self.mutate(lambda d: d.update(parent_hash="abc")))


class TestClaimsNegatives(unittest.TestCase):
    base = {"schema_version": 1, "claims": [{"id": "c", "wording": "w", "source_type": "sourced", "status": "verified",
                                              "sources": ["s"], "scope": "x", "qualifications": [], "checked_at": "t", "owner": "o"}]}

    def test_good(self):
        self.assertEqual(errors("claims", self.base), [])

    def test_verified_needs_source(self):
        d = copy.deepcopy(self.base); d["claims"][0]["sources"] = []
        self.assertTrue(errors("claims", d))

    def test_qualified_needs_qualification(self):
        d = copy.deepcopy(self.base); d["claims"][0]["status"] = "qualified"
        self.assertTrue(errors("claims", d))

    def test_source_type_and_status_are_distinct_dimensions(self):
        d = copy.deepcopy(self.base); d["claims"][0]["status"] = "supplied"
        self.assertTrue(errors("claims", d))
        d = copy.deepcopy(self.base); d["claims"][0]["source_type"] = "verified"
        self.assertTrue(errors("claims", d))


class TestValidateRepoHelpers(unittest.TestCase):
    def test_canonical_hash_is_formatting_independent(self):
        import tempfile, pathlib
        t = pathlib.Path(tempfile.mkdtemp())
        a, b = t / "a.json", t / "b.json"
        a.write_text('{"x":1,"y":[1,2]}'); b.write_text('{\n "y": [1, 2],\n "x": 1\n}')
        self.assertEqual(co.canonical_hash(a), co.canonical_hash(b))
        b.write_text('{"y":[1,3],"x":1}')
        self.assertNotEqual(co.canonical_hash(a), co.canonical_hash(b))


if __name__ == "__main__":
    unittest.main()
