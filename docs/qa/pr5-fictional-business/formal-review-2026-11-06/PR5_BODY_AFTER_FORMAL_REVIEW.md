## Purpose and review base

Add a reusable, evidence-led CRO Page Optimizer and make a proportionate CRO check part of eligible full Hormozi offer workflows, even when the owner does not request CRO by name. Add guided beginner intake and focused expert routing without loading the whole skill library for a narrow task.

**Stacked PR:** This branch targets [draft PR #4](https://github.com/simpliolabs/hormozi-skills/pull/4) at `80822ec44bceb56f00028ab52ff9a420f59a6292`. Review PR #5 **against that base**. PR #4 must receive its own review and merge decision; after it merges, retarget PR #5 to `main` and verify the resulting diff and CI before seeking separate PO merge authorization.

**Current PR #5 HEAD:** `7b37ac381c8bf5fb00d87b8e78e95979afed0630`. Status: **Ready for Review; not approved to merge, deploy or publish.**

## Changed scope

The 28-file PR #5 diff adds:

- `skills/cro-page-optimizer/SKILL.md`, its public framework and Codex skill metadata for standalone CRO diagnosis or the root-owned downstream gate.
- `references/cro-waterfall.md` and read-only `scripts/cro_gate.py` for stage/surface eligibility and proportionate depth. Eligible full runs add root-owned `CRO_REVIEW.md` after offer/pricing/sales work and before SUMMARY/QA. A focused request does not trigger a full waterfall. No new specialist role, task mode or schema is added.
- `references/adaptive-routing.md` and both orchestrator entrypoint instructions for one-question guided intake, exact focused deliverables, selected method loading and honest token reporting.
- A narrow read-only `scripts/check_outputs.py` correction that derives distinct refund/cancellation and delivery cost/financial feasibility findings from `OFFER_DECISIONS` for controlled priced-offer runs, even when the workflow is already HELD or a free-text blocker is generic. The 17 original standalone skill bodies, five existing specialist roles and four schemas remain unchanged.
- Regression tests, first-use/operator documentation, an updated README and two illustrations. The fictional DeskFern test materials retain their original pinned `6b7a04e` prompt and fixture for reproducibility; the corrected candidate evidence is linked below.

## Verification at exact HEAD

- [PR-HEAD GitHub Actions run #42259351692](https://github.com/simpliolabs/hormozi-skills/actions/runs/42259351692): Ubuntu and Windows **passed**, 342 tests and one platform-specific skip per OS, plus repository checks.
- [Corrected native acceptance evidence and 40-criterion matrix](https://github.com/simpliolabs/hormozi-skills/blob/48ee079ad87890d5e2b4641473d21738d1198d97/docs/qa/pr5-fictional-business/native-acceptance-fix-2026-11-06/README.md): A beginner **PASS, bounded**; B five focused hooks **PASS**; C fresh full offer **PASS for all seven obligation identities** with automatic CRO and no operator repair after first completion; D direct CRO **PASS, bounded**. A/B/D were original pinned-source runs independently reviewed, not rerun at this HEAD.
- [PO ready-for-review decision and review requirements](https://github.com/simpliolabs/hormozi-skills/pull/5#issuecomment-6690864005). Independent design, exact-source code and four-case evidence review receipts are preserved in the evidence package. The next gate is formal PR code/release review and a separate merge decision.

## Safety and runtime limits

The corrected C checker returned **HELD** as expected: real-business validation, refund/cancellation, delivery cost/feasibility, PITCH review, HOOKS review, LANDING_PAGE review and the aggregate review blocker remain visible. A structural check does not authenticate owner approval, separate sales-copy review, market truth or publication readiness.

Native specialist dispatch was refused by the host route gate, so only sequential fallback is observed. Native browser rendering in D was denied. Full-offer token use was 1,095,278 cumulative input (1,015,552 cached) and 19,087 output, higher than the original run; there is no measured efficiency gain or hard token cap. No real customer, live site, commercial claim release, deployment or external business-system change was involved.

**Do not merge PR #5 while PR #4 is still draft and unreviewed.** Resolve formal review findings and the stack, then return for PO merge authorization.
