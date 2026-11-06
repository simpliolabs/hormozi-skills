"""SIMULATED regression tests for PR1 review items P0-4, P1-4 and P1-5.

Every test builds synthetic run records and asset files in a temp workspace and asserts on the checker's
findings over the actual bytes. Nothing here was produced by a native Codex or Claude run, so none of it is
evidence of native behaviour; it proves the deterministic gate rejects the leakage. The checker is not relaxed.
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import build_run, codes, read_json, sha, write_json, REPO  # noqa: E402  (puts scripts/ on sys.path)
import check_outputs as co  # noqa: E402
import test_workflows as tw  # noqa: E402

FIX = json.loads((REPO / "tests" / "fixtures" / "review_regression_scenarios.json").read_text(encoding="utf-8"))
T, BLOCKED = FIX["terms"], FIX["blocked_claims"]
ASSETS = ["OFFER", "PRICING", "PITCH", "LANDING_PAGE", "SUMMARY"]
OWNER_FIELDS = ("price", "guarantee", "bonus")
NOW = "2026-11-03T00:00:00Z"


def asset_path(name):
    return f"output/{name}.md"


def body(name):
    if name == "SUMMARY":
        # a full run's summary follows the canonical section contract and still carries the bound owner terms
        return (f"# Summary\n\nPrice: {T['price']['display']}.\nGuarantee: {T['guarantee']['display']}.\n{T['bonus']['display']}.\n"
                f"{FIX['safe_claim']['wording']}.\n\n"
                "## Offer\n\nThe approved offer, as the owner authorized it.\n\n"
                "## Key Decisions\n\nTerms are the owner-approved ones; proposals stay held.\n\n"
                "## Best Hook\n\n> Stop guessing what to say to your first client.\n\n"
                "## Next Actions\n\n1. Confirm the terms with the owner.\n2. Review the pitch.\n3. Send it to five prospects.\n")
    return (f"# {name}\n\nPrice: {T['price']['display']}.\nGuarantee: {T['guarantee']['display']}.\n{T['bonus']['display']}.\n"
            f"{FIX['safe_claim']['wording']}.\n")


def field(kind, value, display, **extra):
    f = {"kind": kind, "value": value, "display": display, "status": "approved", "owner": "owner",
         "updated": NOW, "authorization_ref": "chat:go-1"}
    f.update(extra)
    return f


def proposal(kind, value, display, owner):
    return {"kind": kind, "value": value, "display": display, "status": "proposed", "owner": owner, "updated": NOW}


def claim(c):
    return {"id": c["id"], "wording": c["wording"], "source_type": c["source_type"], "status": c["status"],
            "sources": [], "scope": "release hold", "qualifications": [], "checked_at": NOW, "owner": "root"}


class FiveAssetCase(unittest.TestCase):
    """SIMULATED: a Stage A run whose five customer assets are owned by distinct tasks."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.run_dir, self.ws = build_run(self.tmp)
        for n in ASSETS:
            (self.ws / asset_path(n)).write_text(body(n), encoding="utf-8")
        (self.ws / "output" / "OFFER_AUDIT.md").write_text("audit of the proposal", encoding="utf-8")
        self.write_records()

    def write_records(self):
        ws, run = self.ws, self.run_dir
        src = {"path": "input/offer.md", "sha256": sha((ws / "input/offer.md").read_bytes())}

        def frozen(*paths):
            return [{"path": p, "sha256": sha((ws / p).read_bytes())} for p in paths]

        tasks = [
            {"id": "t_prop", "role": "sub-offer", "mode": "proposal", "status": "done", "depends_on": [], "inputs": [src], "write_set": [asset_path("OFFER")]},
            {"id": "t_aud", "role": "sub-value", "mode": "audit", "status": "done", "depends_on": ["t_prop"], "inputs": frozen(asset_path("OFFER")), "write_set": ["output/OFFER_AUDIT.md"]},
            {"id": "t_price", "role": "sub-pricing", "mode": "final_feasibility", "status": "done", "depends_on": ["t_prop", "t_aud"],
             "inputs": frozen(asset_path("OFFER"), "output/OFFER_AUDIT.md"), "write_set": [asset_path("PRICING")]},
            {"id": "t_sales", "role": "sub-sales", "mode": "copy", "status": "done", "depends_on": ["t_price"],
             "inputs": frozen(asset_path("PRICING")), "write_set": [asset_path("PITCH"), asset_path("LANDING_PAGE")]},
            {"id": "t_sum", "role": "root", "status": "done", "depends_on": ["t_sales"],
             "inputs": frozen(asset_path("PITCH"), asset_path("LANDING_PAGE")), "write_set": [asset_path("SUMMARY")]},
        ]
        owner_task = {"OFFER": "t_prop", "PRICING": "t_price", "PITCH": "t_sales", "LANDING_PAGE": "t_sales", "SUMMARY": "t_sum"}
        prop_price = {"amount_minor": FIX["proposals"]["price"]["amount_minor"], "currency": "USD", "cadence": "one_time"}
        decisions = {"schema_version": 1, "offer_id": "offer1", "version": 3, "parent_hash": None, "fields": {
            "price": field("money", {k: T["price"][k] for k in ("amount_minor", "currency", "cadence")}, T["price"]["display"]),
            "refunds": field("text", "Synthetic approved refund policy", "Synthetic approved refund policy"),
            "cancellation": field("text", "Synthetic approved cancellation policy", "Synthetic approved cancellation policy"),
            "delivery_cost": field("money", {"amount_minor": 100000, "currency": "USD", "cadence": "one_time"},
                                   "$1,000 one-time synthetic cost", evidence=["input/offer.md"]),
            "financial_feasibility": field("text", "Synthetic scoped contribution reviewed",
                                           "Synthetic scoped contribution reviewed", evidence=["input/offer.md"]),
            "cac": field("money", {"amount_minor": 1000, "currency": "USD", "cadence": "one_time"},
                         "$10 one-time synthetic CAC"),
            "guarantee": field("guarantee", T["guarantee"]["value"], T["guarantee"]["display"], conditions=T["guarantee"]["conditions"]),
            "bonus": field("text", T["bonus"]["value"], T["bonus"]["display"]),
            # specialist proposals live beside, never over, the approved terms
            "bonus_proposed": proposal("text", "community", FIX["proposals"]["bonus"]["display"], "sub-value"),
            "guarantee_proposed": proposal("text", "double", FIX["proposals"]["guarantee"]["display"], "sub-sales"),
            "fee_proposed": proposal("money", prop_price, FIX["proposals"]["price"]["display"], "sub-pricing"),
        }}
        write_json(run / "OFFER_DECISIONS.json", decisions)
        write_json(run / "CLAIMS.json", {"schema_version": 1, "claims": [
            {"id": "c_safe", "wording": FIX["safe_claim"]["wording"], "source_type": "supplied", "status": "verified", "sources": [FIX["safe_claim"]["source"]],
             "scope": "all assets", "qualifications": [], "checked_at": NOW, "owner": "root"}] + [claim(c) for c in BLOCKED]})
        brief = read_json(run / "BRIEF.json")
        brief["stage"], brief["requested_artifacts"] = "A", [asset_path(n) for n in ASSETS]
        brief["unknowns"] = []  # this simulated clean-run fixture has approved synthetic economics
        write_json(run / "BRIEF.json", brief)
        arts, reviews = [], []
        for n in ASSETS:
            h = sha((ws / asset_path(n)).read_bytes())
            arts.append({"path": asset_path(n), "sha256": h, "decision_version": 3, "task": owner_task[n], "ready": True, "claim_ids": ["c_safe"],
                         "uses_fields": list(OWNER_FIELDS),
                         "bindings": [{"field": f, "rendered_text": decisions["fields"][f]["display"]} for f in OWNER_FIELDS]})
            reviews.append({"artifact": asset_path(n), "artifact_sha256": h, "decision_version": 3, "reviewer": "adversary", "context": "separate", "result": "pass"})
        st = read_json(run / "RUN_STATE.json")
        st.update(tasks=tasks, artifacts=arts, reviews=reviews, decision_version=3, decision_hash=co.canonical_hash(run / "OFFER_DECISIONS.json"))
        write_json(run / "RUN_STATE.json", st)

    def found(self, mode="ready"):
        return co.validate_run(self.run_dir, self.ws, mode)

    def edit_state(self, fn):
        st = read_json(self.run_dir / "RUN_STATE.json")
        fn(st)
        write_json(self.run_dir / "RUN_STATE.json", st)

    def edit_decisions(self, fn):
        d = read_json(self.run_dir / "OFFER_DECISIONS.json")
        fn(d)
        write_json(self.run_dir / "OFFER_DECISIONS.json", d)
        self.edit_state(lambda s: s.__setitem__("decision_hash", co.canonical_hash(self.run_dir / "OFFER_DECISIONS.json")))

    def resync(self, name):
        """Fresh hash and fresh passing review for one edited asset: only the checker's content rules remain."""
        h = sha((self.ws / asset_path(name)).read_bytes())

        def f(st):
            next(a for a in st["artifacts"] if a["path"] == asset_path(name))["sha256"] = h
            next(r for r in st["reviews"] if r["artifact"] == asset_path(name))["artifact_sha256"] = h
        self.edit_state(f)

    def refreeze(self):
        """Re-hash every frozen task input from current bytes, so only the edited asset's own content rules can fire."""
        def f(st):
            for task in st["tasks"]:
                for i in task["inputs"]:
                    i["sha256"] = sha((self.ws / i["path"]).read_bytes())
        self.edit_state(f)

    def edit_asset(self, name, fn):
        p = self.ws / asset_path(name)
        p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")
        self.resync(name)
        self.refreeze()


class TestSimulatedBlockedClaimLeakage(FiveAssetCase):
    """P0-4: unsupported promises never reach any of the five customer assets."""

    def test_fixture_is_marked_simulated(self):
        self.assertIs(FIX["simulated"], True)
        self.assertIn("Synthetic fixture", FIX["note"])

    def test_clean_five_asset_run_passes_and_contains_no_blocked_wording(self):
        self.assertEqual(self.found(), [])
        for n in ASSETS:
            text = co._norm((self.ws / asset_path(n)).read_text(encoding="utf-8"))
            for c in BLOCKED:
                self.assertNotIn(co._norm(c["wording"]), text, f"{c['id']} leaked into clean {n}")

    def test_each_blocked_claim_is_rejected_in_each_asset_with_fresh_hash_and_review(self):
        for n in ASSETS:
            for c in BLOCKED:
                with self.subTest(asset=n, claim=c["id"]):
                    self.setUp()  # fresh workspace per case
                    self.edit_asset(n, lambda t, w=c["wording"]: t + f"\n{w}.\n")
                    findings = self.found()
                    hit = [f for f in findings if f.code == "CLAIM_UNSUPPORTED_IN_READY" and f.artifact == asset_path(n) and c["id"] in f.reason]
                    self.assertTrue(hit, f"{c['id']} in {n} not rejected: {sorted(codes(findings))}")
                    # a fresh hash and review must not be what let it through, and omission from claim_ids must not hide it
                    self.assertNotIn("ARTIFACT_HASH_MISMATCH", codes(findings))
                    self.assertNotIn("REVIEW_STALE_OR_MISSING", codes(findings))
                    st = read_json(self.run_dir / "RUN_STATE.json")
                    self.assertEqual(next(a for a in st["artifacts"] if a["path"] == asset_path(n))["claim_ids"], ["c_safe"])

    def test_blocked_wording_with_changed_case_and_spacing_is_still_rejected(self):
        for c in BLOCKED:
            with self.subTest(claim=c["id"]):
                self.setUp()
                shouty = "  ".join(c["wording"].upper().split())
                self.edit_asset("LANDING_PAGE", lambda t, w=shouty: t + f"\n{w}\n")
                self.assertIn("CLAIM_UNSUPPORTED_IN_READY", codes(self.found()))

    def test_leak_in_one_asset_does_not_taint_the_other_four(self):
        self.edit_asset("PITCH", lambda t: t + "\n" + BLOCKED[0]["wording"] + "\n")
        bad = {f.artifact for f in self.found() if f.code == "CLAIM_UNSUPPORTED_IN_READY"}
        self.assertEqual(bad, {asset_path("PITCH")})

    def test_leak_is_held_in_draft_mode_for_ready_assets_too(self):
        self.edit_asset("OFFER", lambda t: t + "\n" + BLOCKED[2]["wording"] + "\n")
        self.assertIn("CLAIM_UNSUPPORTED_IN_READY", codes(self.found("draft")))


class TestSimulatedCanonicalTermsSurviveProposals(FiveAssetCase):
    """P1-4: specialist proposals never silently replace owner-approved terms; a drifted asset fails."""

    def test_proposed_bonus_fee_and_guarantee_coexist_with_clean_run(self):
        self.assertEqual(self.found(), [])
        d = read_json(self.run_dir / "OFFER_DECISIONS.json")
        for f in OWNER_FIELDS:
            self.assertEqual((d["fields"][f]["status"], d["fields"][f]["owner"]), ("approved", "owner"))
        for f in ("bonus_proposed", "guarantee_proposed", "fee_proposed"):
            self.assertEqual(d["fields"][f]["status"], "proposed")

    def test_every_asset_carries_every_canonical_term(self):
        d = read_json(self.run_dir / "OFFER_DECISIONS.json")
        for n in ASSETS:
            text = (self.ws / asset_path(n)).read_text(encoding="utf-8")
            for f in OWNER_FIELDS:
                self.assertIn(d["fields"][f]["display"], text)

    def test_binding_a_proposed_term_into_an_asset_is_held(self):
        for prop in ("bonus_proposed", "guarantee_proposed", "fee_proposed"):
            with self.subTest(field=prop):
                self.setUp()
                display = read_json(self.run_dir / "OFFER_DECISIONS.json")["fields"][prop]["display"]

                def f(st):
                    art = next(a for a in st["artifacts"] if a["path"] == asset_path("LANDING_PAGE"))
                    art["uses_fields"].append(prop)
                    art["bindings"].append({"field": prop, "rendered_text": display})
                self.edit_state(f)
                self.assertIn("FIELD_NOT_APPROVED", codes(self.found()))

    def test_proposed_term_silently_replacing_canonical_text_is_held_in_each_asset(self):
        swaps = {"price": (T["price"]["display"], FIX["proposals"]["price"]["display"]),
                 "guarantee": (T["guarantee"]["display"], FIX["proposals"]["guarantee"]["display"]),
                 "bonus": (T["bonus"]["display"], FIX["proposals"]["bonus"]["display"])}
        for n in ASSETS:
            for term, (old, new) in swaps.items():
                with self.subTest(asset=n, term=term):
                    self.setUp()
                    self.edit_asset(n, lambda t, o=old, w=new: t.replace(o, w))
                    self.assertIn("BINDING_TEXT_MISSING", [f.code for f in self.found() if f.artifact == asset_path(n)])

    def test_mutating_price_or_guarantee_in_one_downstream_asset_fails_only_that_asset(self):
        mutations = {"price": (T["price"]["display"], "$1,200 per month"),
                     "guarantee": (T["guarantee"]["display"], "Refund within 30 days no matter what")}
        for n in ASSETS[1:]:
            for term, (old, new) in mutations.items():
                with self.subTest(asset=n, term=term):
                    self.setUp()
                    self.edit_asset(n, lambda t, o=old, w=new: t.replace(o, w))
                    findings = self.found()
                    self.assertTrue(findings, "mutated asset passed")
                    self.assertEqual({f.artifact for f in findings}, {asset_path(n)})

    def test_approved_value_changed_without_updating_assets_is_held(self):
        self.edit_decisions(lambda d: d["fields"]["price"]["value"].__setitem__("amount_minor", FIX["proposals"]["price"]["amount_minor"]))
        self.assertIn("MONEY_RENDER_MISMATCH", codes(self.found()))


class TestSimulatedStageBTwice(tw.RouteCase):
    """P1-4: Stage B twice keeps the frozen original and separate audit/check ownership (existing fixture mechanism)."""

    def test_two_passes_keep_original_frozen_and_audits_separately_owned(self):
        original = sha((self.ws / tw.SRC).read_bytes())
        for _ in range(2):
            st = self.graph("B", tw.B_ROUTE)
            self.assertEqual(self.found(), set())
            diag, check = self.task(st, "t_diag"), self.task(st, "t_check")
            self.assertEqual(diag["inputs"], [{"path": tw.SRC, "sha256": original}])
            self.assertEqual(sha((self.ws / tw.SRC).read_bytes()), original)
            self.assertEqual(diag["write_set"], [tw.DIAG])
            self.assertEqual(check["write_set"], [tw.CHECK])
            self.assertFalse(set(diag["write_set"]) & set(check["write_set"]))
            self.assertNotEqual(diag["id"], check["id"])

    def test_second_pass_cannot_audit_the_revised_offer_as_the_original(self):
        self.graph("B", tw.B_ROUTE)
        revised = self.ws / "output" / "OFFER.md"
        self.edit(lambda s: self.task(s, "t_diag").__setitem__("inputs", [{"path": tw.OFFER, "sha256": sha(revised.read_bytes())}]))
        self.assertIn("ORIGINAL_SNAPSHOT_NOT_AUDITED", self.found())

    def test_second_pass_cannot_overwrite_the_original_audit(self):
        self.graph("B", tw.B_ROUTE)
        self.edit(lambda s: self.task(s, "t_check").__setitem__("write_set", [tw.DIAG]))
        self.assertIn("WRITE_SET_OVERLAP", self.found())

    def test_original_audit_cannot_be_claimed_as_an_artifact_of_the_revised_check_task(self):
        self.graph("B", tw.B_ROUTE)
        a = dict(read_json(self.run_dir / "RUN_STATE.json")["artifacts"][0], path=tw.DIAG, task="t_check")
        self.edit(lambda s: s["artifacts"].append(a))
        self.assertIn("ARTIFACT_OUTSIDE_WRITE_SET", self.found())


class TestSimulatedMatureB2BHolds(FiveAssetCase):
    """P1-5: unknown CAC, refund exposure, delivery cost and affiliate commission stay unknown and uncertified."""

    UNKNOWN = FIX["mature_b2b"]["unknown_fields"]

    def setUp(self):
        super().setUp()

        def f(d):
            for u in self.UNKNOWN:
                d["fields"][u] = {"kind": "money", "value": None, "status": "unknown", "owner": "root", "updated": NOW}
        self.edit_decisions(f)
        brief = read_json(self.run_dir / "BRIEF.json")
        brief["unknowns"] = list(self.UNKNOWN)
        write_json(self.run_dir / "BRIEF.json", brief)
        c = read_json(self.run_dir / "CLAIMS.json")
        c["claims"] += [claim(b) for b in FIX["mature_b2b"]["blocked_claims"]]
        write_json(self.run_dir / "CLAIMS.json", c)

    def test_unknowns_remain_unknown_null_and_root_owned(self):
        d = read_json(self.run_dir / "OFFER_DECISIONS.json")
        for u in self.UNKNOWN:
            self.assertEqual((d["fields"][u]["status"], d["fields"][u]["value"], d["fields"][u]["owner"]), ("unknown", None, "root"))
        self.assertEqual(codes(self.found()), {"COMMERCIAL_COST_FEASIBILITY_UNVERIFIED"})

    def test_no_asset_may_certify_an_unknown_term(self):
        for u in self.UNKNOWN:
            for n in ASSETS:
                with self.subTest(field=u, asset=n):
                    self.setUp()

                    def f(st):
                        art = next(a for a in st["artifacts"] if a["path"] == asset_path(n))
                        art["uses_fields"].append(u)
                        art["bindings"].append({"field": u, "rendered_text": "0"})
                    self.edit_state(f)
                    self.assertIn("FIELD_NOT_APPROVED", codes(self.found()))

    def test_unknown_cannot_be_zeroed_in_the_decision_record(self):
        for u in self.UNKNOWN:
            with self.subTest(field=u):
                self.setUp()
                self.edit_decisions(lambda d, u=u: d["fields"][u].__setitem__("value", 0))
                self.assertTrue(self.found(), "unknown with a zero value must be held")

    def test_margin_refund_and_affiliate_promises_are_blocked_in_every_asset(self):
        for n in ASSETS:
            for b in FIX["mature_b2b"]["blocked_claims"]:
                with self.subTest(asset=n, claim=b["id"]):
                    self.setUp()
                    self.edit_asset(n, lambda t, w=b["wording"]: t + f"\n{w}.\n")
                    self.assertTrue([f for f in self.found() if f.code == "CLAIM_UNSUPPORTED_IN_READY" and f.artifact == asset_path(n) and b["id"] in f.reason])

    def test_owner_approved_non_money_terms_survive_and_currency_stays_consistent(self):
        m = FIX["mature_b2b"]["price"]
        self.edit_decisions(lambda d: d["fields"].__setitem__(
            "price", field("money", {k: m[k] for k in ("amount_minor", "currency", "cadence")}, m["display"])))
        for n in ASSETS:
            self.edit_asset(n, lambda t: t.replace(T["price"]["display"], m["display"]))

        def f(st):
            for a in st["artifacts"]:
                next(b for b in a["bindings"] if b["field"] == "price")["rendered_text"] = m["display"]
        self.edit_state(f)
        self.assertEqual(codes(self.found()), {"COMMERCIAL_COST_FEASIBILITY_UNVERIFIED"})
        self.edit_asset("PITCH", lambda t: t.replace(m["display"], "$4,800 per month"))
        self.assertIn("BINDING_TEXT_MISSING", codes(self.found()))
        d = read_json(self.run_dir / "OFFER_DECISIONS.json")
        self.assertEqual(d["fields"]["bonus"]["display"], T["bonus"]["display"])
        self.assertEqual(d["fields"]["guarantee"]["conditions"], T["guarantee"]["conditions"])


class TestEntryPointsRequireCheckpointAndOwnerResponse(unittest.TestCase):
    """Instruction wording guard (text only, not behaviour): the sparse-idea regression fix stays in all three entry files."""

    FILES = ("skills/hormozi-orchestrator/SKILL.md", "agents/hormozi-orchestrator.md", "references/orchestration.md")

    def test_checkpoint_resume_and_substantive_final_response_are_required_everywhere(self):
        for rel in self.FILES:
            text = (REPO / rel).read_text(encoding="utf-8")
            for needle in ("CHECKPOINT.md", "same conversation", "Value Equation", "validation next steps"):
                self.assertIn(needle, text, f"{rel} lacks {needle!r}")

    def test_root_skill_documents_manual_invocation_without_inventing_switches(self):
        text = (REPO / self.FILES[0]).read_text(encoding="utf-8")
        self.assertIn("absolute path to this `SKILL.md`", text)
        self.assertIn("model/effort switches", text)


if __name__ == "__main__":
    unittest.main()
