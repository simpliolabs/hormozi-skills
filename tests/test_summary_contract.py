"""The canonical output/SUMMARY.md contract, driven through public validate_run and the CLI.

Every case builds real files and run records in a temp workspace. Summary findings carry dedicated SUMMARY_* codes,
so a full run that is held for other reasons cannot hide a missing or malformed summary (and vice versa).
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO, VALID_SUMMARY, add_summary, codes, read_json, sha, write_json
import check_outputs as co
import test_workflows as tw

B_ROUTE, C_ROUTE = tw.B_ROUTE, tw.C_ROUTE
E_SAME_ROLE = [
    ("t_hooks", "sub-sales", "hooks", [], ["output/HOOKS.md"]),
    ("t_sales", "sub-sales", "copy", ["t_hooks"], ["output/PITCH.md"]),
]
E_FOCUSED = [
    ("t_market", "sub-market", None, [], []),
    ("t_offer", "sub-offer", None, [], []),
    ("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"]),
]
SKIPPED = {"t_market": "not_requested", "t_offer": "not_applicable"}


def summary_codes(found):
    return {c for c in codes(found) if c.startswith("SUMMARY_")}


def doc(offer="The approved offer in one paragraph.", decisions="- Price approved.\n- CAC unknown, held.",
        hook="> Stop guessing what to say to your first client.",
        actions="1. Confirm the price.\n2. Measure CAC.\n3. Send the pitch."):
    return (f"# Summary\n\n## Offer\n\n{offer}\n\n## Key Decisions\n\n{decisions}\n\n"
            f"## Best Hook\n\n{hook}\n\n## Next Actions\n\n{actions}\n")


class SummaryCase(tw.RouteCase):
    def request(self, *names):
        b = read_json(self.run_dir / "BRIEF.json")
        b["requested_artifacts"] = list(names)
        write_json(self.run_dir / "BRIEF.json", b)

    def summ(self, **kw):
        add_summary(self.run_dir, self.ws, **kw)

    def found_summary(self, mode="ready"):
        return summary_codes(co.validate_run(self.run_dir, self.ws, mode))


class TestApplicability(SummaryCase):
    def test_full_priced_stages_require_the_summary(self):
        for stage, route in (("A", tw.A_ROUTE), ("B", tw.B_ROUTE), ("D", tw.D_ROUTE)):
            with self.subTest(stage=stage):
                self.graph(stage, route, summary=False)
                found = co.validate_run(self.run_dir, self.ws)
                self.assertIn("SUMMARY_MISSING", codes(found))
                self.assertEqual(codes(found) - {"SUMMARY_MISSING"}, set())  # nothing else is wrong with the run

    def test_multi_step_stage_c_with_two_business_requests_requires_it(self):
        self.graph("C", C_ROUTE, {"t_offer": "not_applicable"}, summary=False)
        self.request("PITCH.md", "HOOKS.md")
        self.assertIn("SUMMARY_MISSING", self.found_summary())

    def test_stage_e_with_two_same_role_active_tasks_requires_it(self):
        self.graph("E", E_SAME_ROLE, summary=False)
        self.request("PITCH.md")
        self.assertIn("SUMMARY_MISSING", self.found_summary())

    def test_explicit_summary_requests_opt_in(self):
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"])], summary=False)
        for names in (["PITCH.md", "SUMMARY.md"], ["PITCH.md", "output/SUMMARY.md"], ["PITCH.md", "OWNER_SUMMARY.md"]):
            with self.subTest(names=names):
                self.request(*names)
                self.assertIn("SUMMARY_MISSING", self.found_summary())

    def test_focused_runs_need_no_summary(self):
        self.graph("C", C_ROUTE, {"t_offer": "not_applicable"}, summary=False)
        self.assertEqual(self.found_summary(), set())
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"])], summary=False)
        self.assertEqual(self.found_summary(), set())

    def test_focused_run_with_skipped_upstream_and_review_bookkeeping_needs_no_summary(self):
        self.graph("E", E_FOCUSED, SKIPPED, summary=False)
        self.request("PITCH.md", "CHECKPOINT.md", "QA_REPORT.md", "output/REVIEW.md", "output/runs/run1/RUN_STATE.json",
                     "BRIEF.json", "OFFER_DECISIONS.json", "CLAIMS.json")
        self.assertEqual(self.found_summary(), set())

    def test_equivalent_request_spellings_count_once(self):
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"])], summary=False)
        self.request("PITCH.md", "output/PITCH.md", "./output/PITCH.md", "output\\PITCH.md", ".\\output\\PITCH.md")
        self.assertEqual(self.found_summary(), set())

    def test_distinct_genuine_paths_stay_distinct(self):
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"])], summary=False)
        self.request("output/PITCH.md", "output\\LANDING_PAGE.md")
        self.assertIn("SUMMARY_MISSING", self.found_summary())

    def test_draft_mode_tolerates_partial_full_run(self):
        self.graph("B", B_ROUTE[:2], summary=False)
        self.assertEqual(self.found_summary("draft"), set())
        self.graph("B", B_ROUTE, summary=False)
        self.assertEqual(self.found_summary("draft"), set())

    def test_ready_false_cannot_skip_the_completion_check(self):
        self.graph("B", B_ROUTE, summary=False)
        self.edit(lambda s: [a.__setitem__("ready", False) for a in s["artifacts"]])
        self.assertIn("SUMMARY_MISSING", self.found_summary())

    def test_held_full_run_still_needs_the_summary(self):
        self.graph("B", B_ROUTE, summary=False)
        self.edit(lambda s: (s.__setitem__("phase", "HELD"), s["blockers"].append("owner has not approved the price")))
        found = co.validate_run(self.run_dir, self.ws)
        self.assertIn("SUMMARY_MISSING", codes(found))
        self.assertIn("BLOCKER_OPEN", codes(found))


class TestCanonicalLocation(SummaryCase):
    def setUp(self):
        super().setUp()
        self.graph("B", B_ROUTE, summary=False)

    def test_valid_canonical_summary_passes(self):
        self.summ()
        self.assertEqual(co.validate_run(self.run_dir, self.ws), [])

    def test_file_on_disk_but_not_in_manifest(self):
        self.summ(manifest=False)
        self.assertIn("SUMMARY_NOT_IN_MANIFEST", self.found_summary())

    def test_manifest_entry_but_file_absent(self):
        self.summ(write_file=False)
        found = co.validate_run(self.run_dir, self.ws)
        self.assertIn("SUMMARY_MISSING", codes(found))
        self.assertIn("ARTIFACT_MISSING", codes(found))

    def test_alias_file_cannot_stand_in(self):
        self.summ(file_path="output/OWNER_SUMMARY.md", manifest_path="output/OWNER_SUMMARY.md", task_id="t_owner")
        self.assertIn("SUMMARY_MISSING", self.found_summary())

    def test_nested_or_wrong_name_files_cannot_stand_in(self):
        for rel in ("output/notes/SUMMARY.md", "output/runs/run1/SUMMARY.md", "SUMMARY.md", "output/SUMMARY.txt", "output/summary-final.md"):
            with self.subTest(rel=rel):
                self.summ(file_path=rel, manifest_path=rel)
                self.assertIn("SUMMARY_MISSING", self.found_summary())

    def test_leading_dot_slash_and_backslash_manifest_paths_are_accepted(self):
        for mp in ("./output/SUMMARY.md", "output\\SUMMARY.md", ".\\output\\SUMMARY.md"):
            with self.subTest(manifest_path=mp):
                self.summ(manifest_path=mp)
                self.assertEqual(self.found_summary(), set())
                self.assertEqual(co.validate_run(self.run_dir, self.ws), [])

    def test_summary_not_owned_by_its_writer_is_held(self):
        self.summ(write_set=[])
        self.assertIn("ARTIFACT_OUTSIDE_WRITE_SET", codes(co.validate_run(self.run_dir, self.ws)))

    def test_unsafe_manifest_path_is_not_the_summary(self):
        self.summ(manifest_path="../SUMMARY.md", write_file=False)
        self.assertIn("SUMMARY_MISSING", self.found_summary())


class TestBoundedMarkdown(SummaryCase):
    def setUp(self):
        super().setUp()
        self.graph("B", B_ROUTE, summary=False)

    def check(self, body, expect):
        self.summ(body=body)  # fresh hash and fresh passing review: only the content contract can object
        got = self.found_summary()
        if expect is None:
            self.assertEqual(got, set(), body)
        else:
            self.assertIn(expect, got, body)

    def test_malformed_summaries_are_rejected_with_the_dedicated_code(self):
        base = doc()
        cases = {
            "no actions section": (base.split("## Next Actions")[0], "SUMMARY_SECTION_MISSING"),
            "level-three heading": (base.replace("## Offer", "### Offer"), "SUMMARY_SECTION_MISSING"),
            "level-one heading": (base.replace("## Offer", "# Offer"), "SUMMARY_SECTION_MISSING"),
            "heading only in a comment": (base.replace("## Best Hook\n\n> Stop guessing what to say to your first client.", "<!--\n## Best Hook\n> hidden\n-->"), "SUMMARY_SECTION_MISSING"),
            "heading only in a code fence": (base.replace("## Best Hook\n\n> Stop guessing what to say to your first client.", "```\n## Best Hook\n> example\n```"), "SUMMARY_SECTION_MISSING"),
            "duplicate heading": (base + "\n## Key Decisions\n\nA second, conflicting section.\n", "SUMMARY_SECTION_DUPLICATE"),
            "empty offer": (doc(offer=""), "SUMMARY_SECTION_EMPTY"),
            "comment-only body": (doc(decisions="<!-- decisions go here -->"), "SUMMARY_SECTION_EMPTY"),
            "multiline comment-only body": (doc(offer="<!--\nwrite the offer\n-->"), "SUMMARY_SECTION_EMPTY"),
            "code-only body": (doc(decisions="```\n- Price approved.\n```"), "SUMMARY_SECTION_EMPTY"),
            "hook is a bare path": (doc(hook="output/HOOKS.md"), "SUMMARY_HOOK_UNSTATED"),
            "hook is a bare link": (doc(hook="[the hooks](HOOKS.md)"), "SUMMARY_HOOK_UNSTATED"),
            "hook is see-file": (doc(hook="See HOOKS.md"), "SUMMARY_HOOK_UNSTATED"),
            "hook is quoted see-file": (doc(hook="> see output/HOOKS.md for the hook"), "SUMMARY_HOOK_UNSTATED"),
            "two actions": (doc(actions="1. Confirm the price.\n2. Measure CAC."), "SUMMARY_ACTIONS_INVALID"),
            "four actions": (doc(actions="1. a one\n2. b two\n3. c three\n4. d four"), "SUMMARY_ACTIONS_INVALID"),
            "actions out of order": (doc(actions="1. a one\n3. c three\n2. b two"), "SUMMARY_ACTIONS_INVALID"),
            "actions numbered from two": (doc(actions="2. b two\n3. c three\n4. d four"), "SUMMARY_ACTIONS_INVALID"),
            "bullets are not ordered actions": (doc(actions="- a one\n- b two\n- c three"), "SUMMARY_ACTIONS_INVALID"),
            "empty third marker": (doc(actions="1. a one\n2. b two\n3."), "SUMMARY_ACTIONS_INVALID"),
            "nested items do not make three": (doc(actions="1. a one\n   2. b two\n   3. c three"), "SUMMARY_ACTIONS_INVALID"),
        }
        for name, (body, expect) in cases.items():
            with self.subTest(name):
                self.check(body, expect)

    def test_comment_and_fence_only_sections_are_empty(self):
        for name, actions in (("comment", "<!-- 1. a\n2. b\n3. c -->"), ("fence", "```\n1. a\n2. b\n3. c\n```")):
            with self.subTest(name):
                self.check(doc(actions=actions), "SUMMARY_SECTION_EMPTY")

    def test_well_formed_variants_pass(self):
        base = doc()
        variants = {
            "case-insensitive headings": base.replace("## Offer", "## OFFER").replace("## Next Actions", "## next actions"),
            "closing markers and trailing space": base.replace("## Next Actions", "## Next Actions ##  ").replace("## Offer", "## Offer   "),
            "plain paragraph hook": doc(hook="Stop guessing what to say to your first client."),
            "multiline blockquote hook": doc(hook="> Stop guessing what to say\n> to your first client."),
            "hook with link and real text": doc(hook='> "Stop guessing what to say" - see [hooks](HOOKS.md)'),
            "paren markers": doc(actions="1) Confirm the price.\n2) Measure CAC.\n3) Send the pitch."),
            "continuations and nested explanation": doc(actions=(
                "1. Confirm the price with the owner\n   so nothing ships unapproved.\n   - Reason: the price is held.\n"
                "2. Measure CAC.\n   1. Pull the ad spend.\n   2. Divide by leads.\n3. Send the pitch.")),
            "nested heading and extra section": base.replace("## Offer\n\n", "## Offer\n\n### Details\n\nWhy it works.\n\n") + "\n## File Index\n\n- output/PITCH.md\n",
            "order does not matter": "# S\n\n## Next Actions\n\n1. a one\n2. b two\n3. c three\n\n" + base.split("# Summary\n\n")[1].split("## Next Actions")[0],
            "comment and fence beside real text": doc(offer="<!-- note -->\nThe approved offer.\n\n```\nexample\n```"),
            "heading copy hidden in comment": base + "\n<!--\n## Next Actions\n-->\n",
            "honest unknowns and holds": doc(decisions="- Price: unknown, held for the owner.\n- Guarantee: not approved."),
            "crlf line endings": base.replace("\n", "\r\n"),
        }
        for name, body in variants.items():
            with self.subTest(name):
                self.check(body, None)

    def test_ready_false_does_not_excuse_a_malformed_summary(self):
        self.summ(body=doc(actions="1. only one"), ready=False)
        self.assertIn("SUMMARY_ACTIONS_INVALID", self.found_summary())


class TestDifferentialAndFreshness(SummaryCase):
    def setUp(self):
        super().setUp()
        self.graph("B", B_ROUTE, summary=False)

    def test_complete_summary_removes_only_summary_findings(self):
        self.edit(lambda s: s.__setitem__("reviews", []))  # an unrelated, independent hold on the PITCH
        before = codes(co.validate_run(self.run_dir, self.ws))
        self.summ()
        after = codes(co.validate_run(self.run_dir, self.ws))
        self.assertIn("SUMMARY_MISSING", before)
        self.assertEqual(before - after, {"SUMMARY_MISSING"})
        # the missing review is a sales output, so the independent-review floor reports it alongside the generic finding
        self.assertEqual(after, {"REVIEW_STALE_OR_MISSING", "HIGH_RISK_NO_INDEPENDENT_REVIEW", "BLOCKER_OPEN"})

    def test_stale_bindings_are_rejected_independently_of_content(self):
        self.summ()
        cases = {
            "bytes changed after hashing": (lambda: (self.ws / "output/SUMMARY.md").write_text(VALID_SUMMARY + "\nExtra.\n", encoding="utf-8"), "ARTIFACT_HASH_MISMATCH"),
            "older decision version": (lambda: self.edit(lambda s: next(a for a in s["artifacts"] if a["path"] == "output/SUMMARY.md").__setitem__("decision_version", 2)), "ARTIFACT_DECISION_STALE"),
            "review bound to old bytes": (lambda: self.edit(lambda s: next(r for r in s["reviews"] if r["artifact"] == "output/SUMMARY.md").__setitem__("artifact_sha256", "0" * 64)), "REVIEW_STALE_OR_MISSING"),
        }
        for name, (mutate, expect) in cases.items():
            with self.subTest(name):
                self.setUp()
                self.summ()
                mutate()
                found = codes(co.validate_run(self.run_dir, self.ws))
                self.assertIn(expect, found)
                self.assertEqual(summary_codes(co.validate_run(self.run_dir, self.ws)), set())

    def test_missing_review_is_held(self):
        self.summ(review=False)
        self.assertIn("REVIEW_STALE_OR_MISSING", codes(co.validate_run(self.run_dir, self.ws)))


class TestCli(SummaryCase):
    def run_cli(self, mode="ready"):
        p = subprocess.run([sys.executable, str(REPO / "scripts" / "check_outputs.py"), "--run", str(self.run_dir),
                            "--workspace", str(self.ws), "--mode", mode, "--json"], capture_output=True, text=True, encoding="utf-8")
        return p.returncode, {f["code"] for f in json.loads(p.stdout)}

    def test_cli_holds_a_full_run_without_a_summary_and_passes_with_one(self):
        self.graph("B", B_ROUTE, summary=False)
        rc, found = self.run_cli()
        self.assertEqual((rc, found), (1, {"SUMMARY_MISSING"}))
        self.summ()
        self.assertEqual(self.run_cli(), (0, set()))

    def test_cli_holds_a_malformed_summary(self):
        self.graph("B", B_ROUTE, summary=False)
        self.summ(body=doc(hook="See HOOKS.md"))
        rc, found = self.run_cli()
        self.assertEqual((rc, found), (1, {"SUMMARY_HOOK_UNSTATED"}))

    def test_cli_draft_and_focused_runs_still_pass(self):
        self.graph("B", B_ROUTE, summary=False)
        self.assertEqual(self.run_cli("draft"), (0, set()))
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"])], summary=False)
        self.assertEqual(self.run_cli(), (0, set()))


def fs_is_case_sensitive():
    probe = Path(tempfile.mkdtemp())
    try:
        (probe / "a").write_text("x", encoding="utf-8")
        return not (probe / "A").exists()
    finally:
        shutil.rmtree(probe, ignore_errors=True)


class TestCorrectionP2(SummaryCase):
    """Independent code review P2 findings, through public validate_run with fresh hashes and reviews."""

    def two_artifacts(self, second):
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md", f"output/{second}"])], summary=False)

        def f(st):
            h = sha((self.ws / "output" / second).read_bytes())
            st["artifacts"].append({"path": f"output/{second}", "sha256": h, "decision_version": st["decision_version"],
                                    "task": "t_sales", "ready": True})
            st["reviews"].append({"artifact": f"output/{second}", "artifact_sha256": h, "decision_version": st["decision_version"],
                                  "reviewer": "adversary", "context": "separate", "result": "pass"})
        self.edit(f)
        self.request("PITCH.md", second)

    def test_real_review_named_business_output_is_counted(self):
        for second in ("REVIEW_OFFER.md", "CUSTOMER_RECEIPT.md"):
            with self.subTest(second):
                self.setUp()  # fresh workspace per case: artifacts from the earlier case would lose their write set
                self.two_artifacts(second)
                found = codes(co.validate_run(self.run_dir, self.ws))
                self.assertNotIn("REQUESTED_ARTIFACT_MISSING", found)
                self.assertIn("SUMMARY_MISSING", found)

    def test_known_bookkeeping_names_stay_excluded_case_insensitively(self):
        self.graph("E", E_FOCUSED, SKIPPED, summary=False)
        self.request("PITCH.md", "checkpoint.MD", "Qa_Report.md", "output/review.md", "BRIEF.JSON")
        self.assertEqual(self.found_summary(), set())

    def summary_with(self, **kw):
        self.graph("B", B_ROUTE, summary=False)
        self.summ(body=doc(**kw))
        return self.found_summary()

    def test_actual_hook_text_beginning_with_see_beside_a_source_link_passes(self):
        self.assertEqual(self.summary_with(hook='> "See your offer clearly."\n\nSource: [hooks](HOOKS.md)'), set())

    def test_label_wrapped_reference_only_hook_is_unstated(self):
        for hook in ("Chosen hook: [the selected hook](HOOKS.md)", "> Selected hook: output/HOOKS.md", "Hook: see [HOOKS](HOOKS.md)"):
            with self.subTest(hook):
                self.assertIn("SUMMARY_HOOK_UNSTATED", self.summary_with(hook=hook))

    def test_unrelated_paragraph_cannot_fill_an_empty_action(self):
        got = self.summary_with(actions="1. Confirm the price.\n2. Measure CAC.\n3.\n\nAdditional context outside the list.")
        self.assertIn("SUMMARY_ACTIONS_INVALID", got)

    def test_three_space_top_level_list_with_wrapped_and_nested_text_passes(self):
        actions = ("   1. Confirm the price\n      with the owner.\n      - Reason: it is held.\n"
                   "   2. Measure CAC.\n      1. Pull spend.\n   3. Send the pitch.")
        self.assertEqual(self.summary_with(actions=actions), set())

    def test_shallower_fourth_marker_makes_the_whole_list_four_top_level_items(self):
        for pad in (" ", "   "):
            with self.subTest(indent=len(pad)):
                actions = f"{pad}1. Confirm the price.\n{pad}2. Measure CAC.\n{pad}3. Send the pitch.\n4. Review the results."
                self.assertIn("SUMMARY_ACTIONS_INVALID", self.summary_with(actions=actions))

    @unittest.skipUnless(fs_is_case_sensitive(), "needs a case-sensitive filesystem")
    def test_case_distinct_requests_are_two_deliverables_on_case_sensitive_systems(self):
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md", "output/pitch.md"])], summary=False)
        self.request("output/PITCH.md", "output/pitch.md")
        self.assertIn("SUMMARY_MISSING", self.found_summary())

    @unittest.skipIf(fs_is_case_sensitive(), "needs a case-insensitive filesystem")
    def test_case_variants_are_one_deliverable_on_case_insensitive_systems(self):
        self.graph("E", [("t_sales", "sub-sales", "copy", [], ["output/PITCH.md"])], summary=False)
        self.request("output/PITCH.md", "output/pitch.md")
        self.assertEqual(self.found_summary(), set())

    def test_repeated_summary_declaration_keeps_one_review(self):
        self.graph("B", B_ROUTE, summary=False)
        self.summ()
        self.summ()
        st = read_json(self.run_dir / "RUN_STATE.json")
        self.assertEqual(len([r for r in st["reviews"] if r["artifact"] == "output/SUMMARY.md"]), 1)


if __name__ == "__main__":
    unittest.main()
