# Exact-fix closure review

CHANGES_REQUIRED for commit `c1b3431a775698eefff5e46a44ddcfc2e3bff9e0`, base `3292a949dd86f9c13989116284819da79de89550`. One remaining P2 concerns the corrected action parser; make that local correction and regression before the fresh native acceptance run.

Task class adversary; gpt-6-astra/xhigh. Independent review of the actual frozen diff and public validation behavior. No repository source edits, delegation, model runs, GitHub writes, merge, deployment or commercial release. Initial HEAD matched the requested commit and the worktree was clean; a later status check after verification was also clean.

## Remaining required correction

**P2 / Important: a shallower fourth action is silently ignored after an indented list.** The new baseline condition collects only markers whose indentation equals the first marker; every nonmatching marker is ignored, including shallower ones that cannot be nested explanation. Consequently the three collected numbers satisfy the final check even when an additional visible action is present. Evidence: `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:565`; `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:568`. This does not implement the newly documented consistent-baseline grammar: `handoff/hormozi-one-chat-2026-11-03/repository/references/orchestration.md:79`.

Public reproduction: create a valid stage-B run through `SummaryCase.graph('B', B_ROUTE, summary=False)`, then `summ(body=doc(actions=...))`, which writes fresh artifact/hash/review records, and call `validate_run(run_dir, ws)`. Both of these four-action bodies return **no findings at all**:

```text
   1. Confirm price.
   2. Measure CAC.
   3. Send pitch.
4. Launch the campaign.
```

The same body with one leading space on its first three lines also returns no findings. Controls establish the boundary: three equally indented actions pass; four equally indented actions produce `SUMMARY_ACTIONS_INVALID`; three actions with a deeper nested explanation pass. All five public probe results, including exact input bodies and all findings, are preserved in `CODE_FIX_CLOSURE_PROBES.json` (SHA256 `a75aff7040e4cc6145edf347e3537985fe5c5a4255c515d7a352714bd0b39d1f`).

Required scope: reject shallower ordered markers after establishing the baseline, while preserving deeper nested explanation and the existing three valid items. Add the public regression with both one-space and three-space baselines and fresh manifests/reviews. This is a correction to the existing conditional, not a reason for a Markdown dependency, new workflow or wider platform work. The current regression covers a three-space positive but lacks the shallower-marker interaction: `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:358`.

## Corrections that close

- Bookkeeping is now an explicit known-name set plus declared receipt paths; REVIEW_OFFER.md and CUSTOMER_RECEIPT.md count as business outputs and cause the missing-summary hold. Case-insensitive known bookkeeping remains excluded. Source and public regressions: `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:451`; `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:469`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:327`.
- The quoted hook beginning with “See” plus a separate source-link paragraph passes, and the three ordinary label-wrapped reference-only variants are held. Paragraph separation and the bounded English label heuristic implement those exact cases: `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:539`; `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:552`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:346`.
- Empty action text cannot be supplied by a separate paragraph, and a consistently three-space-indented list with wrapped/nested explanation passes. Those original counterexamples close, with the interaction above still open: `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:567`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:354`.
- Request identity now uses `os.path.normcase`, matching the existing ownership policy rather than unconditional case folding; summary/control recognition remains separately case-insensitive. The Windows converse test passes, while the real case-sensitive-filesystem test is skipped here: `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:466`; `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:255`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:363`.
- Repeated fixture summary declarations replace the matching review, and the new deduplication regression passes: `handoff/hormozi-one-chat-2026-11-03/repository/tests/helpers.py:143`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:375`.

The fresh integration checks preserve focused/draft behavior, mandatory full-run summaries, canonical location, alias rejection, manifest declaration, writer ownership, hash/decision/review freshness, ready=false handling and unrelated holds. These are exercised through public validation and the CLI: `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:55`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:122`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:242`; `handoff/hormozi-one-chat-2026-11-03/repository/tests/test_summary_contract.py:277`. The implementation still runs ordinary artifact enforcement before summary enforcement: `handoff/hormozi-one-chat-2026-11-03/repository/scripts/check_outputs.py:163`.

## Commands and evidence

Executed from the repository's `tests/` directory:

```text
python -m unittest test_summary_contract.TestCorrectionP2 test_summary_contract.TestBoundedMarkdown -v
python -m unittest test_summary_contract.TestApplicability test_summary_contract.TestCanonicalLocation test_summary_contract.TestDifferentialAndFreshness test_summary_contract.TestCli -v
```

First command: 13 tests in 7.898 seconds, OK, one case-sensitive-filesystem skip. Second: 25 tests in 2.885 seconds, OK. Combined: all 38 existing targeted tests executed, 37 passed and one skipped. Exit codes were zero. Logs: `CODE_FIX_CLOSURE_TARGETED.txt` SHA256 `7dc6384ad9b6ca94983b2fbcad1ea987fa5e182a6dc9c9f00daea340c1340faa`; `CODE_FIX_CLOSURE_INTEGRATION.txt` SHA256 `b6a3cd7d056a26845aa81069afb798ddc872f38705110915b38b17d78ca91b0a`.

Executed `python scripts/check_outputs.py --repo .` from the repository: PASS. Executed the five additional public validation probes above via `python -` from `tests/`: two false passes, three expected controls. Those probes, not a failing existing test, establish the remaining finding.

Inspected and reused worker evidence without repeating the full suite: `correction_green_full.txt` records 245 tests, OK (skipped=1), SHA256 `19e59fb6ff34d8c30876ed6af755121bd2005823863381d7710c55e939bad447`; `correction_red.txt` records nine tests, eight assertion failures and one skip before the production correction. The frozen replay remains four BLOCKER_OPEN, three HIGH_RISK_NO_INDEPENDENT_REVIEW and SUMMARY_MISSING; `correction_native_replay.json` SHA256 `ac47d65e00443f4739322ba8232950a8dd7ca99b03f8745ed489d68f2cc51272`. This is replay evidence, not fresh native acceptance.

## Pins and limits

- Reviewed prior `CODE_REVIEW.md` SHA256 `96c73e8d261cd3c01a0c2ebd6866c9ebb3cbb139c2aea20f58887a5fa1d6677f`, and `CORRECTION_REPORT.md` SHA256 `c1b281d1b2f510f01babf9a3b57d86ef44229e0ffa747318a1e6ef60c9524f7e`. The correction report's “uncommitted” statement predates the pinned commit; it is not the reviewed HEAD status.
- Reviewed checker SHA256 `49a231c5ff0b1756ed69fc7dff2d155f5d1014cf10ae22f64f259f1d43281753`.
- No native Linux/case-sensitive-filesystem execution, no fresh installed-candidate acceptance, no native-wrapper success claim and no inference about model billing.
- The English label heuristic remains bounded; semantic hook choice, arbitrary reference prose and action priority remain review responsibilities. This review does not claim an arbitrary marketing-semantic guarantee.
- The unchanged business methods, specialists, schema, dependencies and old benchmarks were not reopened. Accepted necessity and scope stand; only the concrete action-parser finding requires correction.

Citation verification command: `python "2hm research/tools/verify_citations.py" handoff/hormozi-one-chat-2026-11-03/summary-contract-fix-2026-11-04/CODE_FIX_CLOSURE.md`; 22 citations resolved in the intended workspace tree, zero failures.

Retain the original first-completion native acceptance and all existing business/review holds after this narrow closure correction.
