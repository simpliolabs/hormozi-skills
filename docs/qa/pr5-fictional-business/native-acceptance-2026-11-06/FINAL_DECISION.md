# PR #5 developer native acceptance result

**Exact tested SHA:** `6b7a04e949e4ed69019591acab9f616107348b7c` on `feature/cro-page-optimizer-waterfall`; installed plugin's 177 tracked files byte-matched the pinned Windows checkout. Source checkout remained clean. PR #5 was still open and draft at the final read boundary.

| Scenario | Operator result | Direct evidence |
| --- | --- | --- |
| A Beginner | **PASS**, bounded | Natural language loaded orchestrator/adaptive routing, first reply asked one useful question, same-thread owner follow-up stayed concise. The initial A2 CLI resume failed before model execution; corrected A2R succeeded but was read-only, so file persistence and the complete beginner journey are unproven. |
| B Expert | **PASS** | Exactly five hooks; only hooks skill loaded; no offer waterfall or CRO artifact. |
| C Full offer | **FAIL** overall | Automatic CRO skill and read-only readiness gate ran, `CRO_REVIEW.md` and canonical `SUMMARY.md` were produced, and sales output stayed HELD. The structured commercial blocker does not explicitly identify refund/cancellation and unknown costs as the historical seven-obligation fixture does. |
| D Direct CRO | **PASS**, bounded | Direct skill loaded and diagnosed 1040px mobile overflow, silent 9.5-second submit, dead sign-in and unsupported 5,000+ proof; synthetic analytics were treated as non-causal. Native browser access was denied, and no native screenshot/render claim was made. Separate operator Chrome rendering measured mobile overflow. |

## Original outputs and controls

- `sessions/C/first_completion/first_completion.zip` contains the 17 output files frozen immediately at first model completion; SHA256 `1926377e0ac963c489e7b47b81f4529b686ab44727991cd2b94ba8a3f30da736`. `first_completion_hashes.json` has per-file hashes. Read-only checker after capture changed zero files (`post_checker_hash_check.json`).
- Pinned checker on C returned exit 1, **HELD**, six findings: three `BLOCKER_OPEN` (fictional business validation, generic commercial, aggregate review) and three `HIGH_RISK_NO_INDEPENDENT_REVIEW` (PITCH, HOOKS, LANDING_PAGE). No independent sales-copy pass was fabricated or accepted.
- Historical committed PR3 fixture replayed with the pinned checker: exit 1, six findings representing seven explicit identities; its combined business blocker says `Refund/cancellation policy undecided; unknown costs held.` C's structured commercial blocker says only `Commercial terms and financial feasibility require owner approval and evidence`. C copy/decision files disclose the terms, but the checker finding loses their names. `replay/historical_checker.json` and archive SHA receipt preserve the comparison.
- Native C specialist dispatch was attempted once and refused by host `MODEL ROUTE GATE`; root completed sequentially. This proves fallback, **not** differentiated specialist-model execution. D native browser permission was denied; source-backed diagnosis remains useful, while native rendered-page QA is unproven.
- A/B/D had no `output/` directory; their first replies, raw events and full first-workspace ZIPs are preserved. A's failed CLI invocation is preserved separately. No post-completion operator edits to `RUN_STATE`, `CHECKPOINT` or `QA_REPORT` occurred.

## Automated and runtime observations

- Local pinned-source QA: **327 tests passed, one host-specific skip**, plus repository checker and five CRO-gate helper probes (`local_qa/`). GitHub exact-SHA Windows and Ubuntu checks were successful at final read boundary. Green CI does not cure the C acceptance failure.
- Host-observed first-turn usage: A 92,056 input / 426 output tokens in 36.58 s; B 56,820 / 258 in 18.92 s; C 1,042,544 / 12,634 in 391.84 s; D 279,521 / 3,491 in 146.14 s. C cached 979,584 input tokens. A follow-up used 126,362 input / 627 output in 13.92 s. See `TOKEN_LEDGER.csv` for cache/reasoning counters and receipt pointers. No per-skill token attribution or savings claim is made. B used a focused route, but absolute token efficiency is not proven.
- Separate Claude acceptance reviewer inspected C and called the seven-hold result PARTIAL; A/B/D remained uninspected in that review. Its incorrect claim that the C CRO gate was not executed was checked and corrected against the raw completed command event. See `INDEPENDENT_REVIEW.md`.

## Defect and recommendation

**Acceptance defect:** First-completion control state allows a generic commercial blocker to stand in for the two specific refund/cancellation and unknown-cost identities. This is an AI-authored semantic declaration versus deterministic checker boundary. The original historical fixture still passes; the fresh run does not prove first-pass explicit preservation of all seven identities.

**Recommendation: KEEP PR #5 DRAFT / FIX AND RETEST.** Decide the narrow correction at the existing intake/control boundary, retain all business and independent-review holds, then run a fresh unchanged DeskFern C prompt on the corrected branch and independently review all four scenario results before requesting merge readiness. This repeated hold-control issue triggers the workspace architecture-design gate; no source patch was made during this pinned acceptance run. Do not equate sequential fallback with differentiated execution or release commercial claims.

No merge, deployment, commercial publication or external business-system change occurred. This report is a test finding, not a PO merge decision.
