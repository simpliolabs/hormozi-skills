# CRO in the offer upstream/downstream waterfall

This file is normative for the **root orchestrator** in multi-step offer work. It augments, but does not replace, `<plugin_root>/references/orchestration.md` and `<plugin_root>/contracts/`. The CRO step adds no specialist role, task mode, schema or CRO-specific checker rule; the separate commercial-hold correction does extend the read-only checker.

## The automatic gate

**Default = CRO readiness ON** in full stage A, B, D or custom/mixed E multi-step offer workflows, whether or not the user says CRO. For stage C, enable it when the requested sales assets include a landing page, website, signup, checkout, digital funnel, or another identifiable post-click destination. When the requested work is a single focused skill task, keep the default focused and do not trigger a full CRO pipeline.

For a consistent eligibility/depth classification, the root may run the **read-only** helper `python <plugin_root>/scripts/cro_gate.py --stage A --surface planned` (replace the actual stage/surface). Use `--digital-destination` for stage C when an online conversion destination is in scope; use `--no-offer-workflow` for a stage E custom request that is not offer work. A focused single-skill request uses `--focused`. The helper never changes RUN_STATE or business facts and its `depth` is **not** an allowed task `mode`. If Python is unavailable, apply this table directly and record the missing helper, rather than silently skipping CRO.

The gate is **not optional** for eligible full runs: include `CRO_REVIEW.md` in the initial `BRIEF.requested_artifacts` and root task `write_set`; evaluate the conversion path. This remains true even without a live page. Choose depth based on actual evidence:

| Business situation | Root CRO evaluation | Evidentiary limits |
|---|---|---|
| Existing page / checkout | Full six-gate page review of supplied sources and behavior data | Mark any inaccessible DOM, missing metrics and unrendered widths `NOT ASSESSED` |
| New online offer with future page | Conversion-readiness preflight using current offer, planned funnel and sales drafts | Do not invent page screenshots, analytics or conversions |
| Offline / referral-based offer | Minimal offer-to-buyer handoff, with page and SEO fields `NOT APPLICABLE` | Do not manufacture a website, SEO need or A/B test |
| Stage C pitch-only without destination | Minimal handoff or `NOT APPLICABLE` with recorded reason | No spurious full page audit |
| Focused five hooks / one copy edit | Do not force CRO gate; use requested skill | A full CRO audit is available via explicit invocation |

`CRO_REVIEW.md` is a **root-authored diagnostic record**, never a published page or substitute for `LANDING_PAGE.md`. The root loads the real `<plugin_root>/skills/cro-page-optimizer/SKILL.md` and its references before the gate; don't infer the method from this routing file alone.

## Dependency order and feedback

```text
owner brief / existing sources
   -> market (when needed)
   -> offer draft or diagnostic -> value audit -> pricing feasibility
   -> root approvals / reconciliation
   -> requested sales copy / landing page
   -> CRO gate [default for eligible offer work]
       |-- FIX (verified defect or incorrect term): repair shared baseline or hold
       |-- TEST (unproven copy/layout): define optional experiment, do not silently implement
       |-- GAP (missing information): label unknown/not assessed, request evidence
       |-- NO PAGE (online preflight) or OFFLINE (minimal handoff): document scope
   -> re-open affected upstream step only if required and authorized
   -> downstream revalidation + fresh checks and necessary separate reviews
   -> canonical SUMMARY -> final checker -> owner response
```

A **CRO observation never becomes an automatic commercial edit**. If it suggests a different outcome, offer component, scope, membership price, guarantee, eligibility, payment timing or other material term, root proposes the change and requests owner authorization. An upstream revision invalidates affected dependent artifacts, hashes, claims and reviewer receipts; re-run relevant downstream tasks in the allowed existing modes with disjoint write sets. Respect the existing two-repair-pass limit.

## How to record the gate without changing schemas

1. On initial full-run route, root adds `CRO_REVIEW.md` to `BRIEF.requested_artifacts` and its **own** `RUN_STATE.tasks[].write_set` (root role already exists).
2. Do **not** create `sub-cro` roles, `mode: cro`, new workflow phases or claims of native CRO specialist dispatch. The root performs the gate as its QA-stage method application.
3. When the relevant sales draft is accepted, freeze/inspect those inputs and the approved offer decision version. Run the method and write `output/CRO_REVIEW.md` from the actual evidence. It must say `full page audit`, `offer readiness`, `minimal handoff` or `not applicable` explicitly and record its inputs/limitations.
4. Record `CRO_REVIEW.md` in the artifact manifest with real path, file hash, decision version and root task. Add gate findings/holds and method loading to `QA_REPORT.md` and `CHECKPOINT.md` as needed; state the CRO recommendation and unresolved facts in `SUMMARY.md -> Key Decisions` without changing its four canonical headings.
5. The default `CRO_REVIEW.md` contains diagnosis and hypotheses, **not** final publication copy. If it includes ready-to-publish sales wording or high-risk claims, mark it `high_risk: true` and require the same genuine separate-context review floor; otherwise keep proposed words unmistakably provisional. Never use a renamed CRO artifact to evade the sales artifact review floor.
6. When missing CRO inputs prevent even a reasonable offer/buyer-path assessment, keep a transparent diagnostic gap and any applicable real business blocker in RUN_STATE, CHECKPOINT and QA_REPORT. Missing screenshot data alone is **not** grounds to fabricate a new blocker or call the checker READY.
7. The checker remains read-only, but the commercial-hold floor is extended for controlled priced-offer runs. CRO eligibility is an instruction-level root obligation: if root omits CRO from the brief entirely, the checker does not independently detect that omission. In ready mode with valid `BRIEF` and `RUN_STATE` records, existing manifest and file checks require `CRO_REVIEW.md` once it is declared in `BRIEF.requested_artifacts`; an invalid or missing control record is separately an error. Structural `READY` is not CRO success, claim verification, independent reviewer authentication or commercial publication authority.

## Route examples (unambiguous)

- **Stage A, idea for an online subscription:** market -> offer -> value -> pricing -> approved sales drafts -> CRO *readiness* -> SUMMARY + QA. No page exists, so no mobile screenshots claimed.
- **Stage B, live page with drop-off:** original offer diagnostic -> revision -> revised check -> final feasibility -> sales -> CRO *full audit*. Verified broken submit becomes a shared baseline repair; a cleaner hero is a new experiment hypothesis.
- **Stage C, landing copy from already-approved offer:** sales -> CRO *page readiness* -> QA. Do not reprice.
- **Stage D, offline consulting offer:** pricing/offer revisions -> sales -> CRO *minimal buyer handoff*. SEO/page checks are not applicable, but decision and effort friction can still be assessed.
- **Stage E, one-off five hooks:** focused skill only; no full run artifacts or CRO requirement.
- **Explicit CRO request:** invoke CRO skill immediately and only load upstream methods when the evidence demands an offer revision.

## Regression invariants

Maintain the original 17 business skill bodies, five specialist roles, four contracts, defined modes, sales independent-review floor, business limitation declaration, first-completion seven-hold identity evidence, and exactly-four-section canonical SUMMARY contract. The new CRO gate is additive; it cannot clear or replace existing holds.
