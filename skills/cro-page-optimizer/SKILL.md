---
name: cro-page-optimizer
description: Evidence-led conversion rate optimization and SEO-to-conversion review for websites, landing pages, forms, checkouts and offer-to-sales handoffs. Use for "improve my conversion rate", "audit this page", "review Clarity/analytics", "fix mobile drop-off", "plan an A/B test", "improve search-intent match" or "what should we fix first?". Also load as the default downstream CRO readiness gate in a multi-step Hormozi offer workflow even when CRO was not explicitly requested; audit an actual page only if one exists.
---

# CRO Page Optimizer

## Purpose

Find **the first real barrier to a qualified conversion**, not merely the first phrase to rewrite. This original, generalized skill borrows the six-gate approach of CEO Creative SEO + CRO while retaining the public Hormozi evidence and decision contracts. It is not an official PPC.io/Postclick skill. Do not include client-specific terms, brand designs, hidden analytics, or private customer data as universal facts.

## Authority and inputs

- Load `<plugin_root>/references/evidence-contract.md` and `<plugin_root>/skills/cro-page-optimizer/references/CRO_FRAMEWORK.md` before judging a page. In orchestrated runs also load `<plugin_root>/references/cro-waterfall.md`.
- Preserve exact original copy, legal terms, CTA destinations, URLs, screenshots and page markup. Distinguish owner-approved terms from proposed improvements. Owner approval does not make a claim factually verified.
- Accept whichever evidence actually exists: page URL or saved HTML, mobile/desktop screenshots, search query or traffic source, offer facts, heatmaps/Clarity summaries, funnel events, user recordings, conversion counts, and technical errors. Clearly note sources, dates, sample sizes and missing inputs; **never fabricate** buyer reactions, competitors, traffic, conversion uplifts, rankings, testimonials or screenshots.
- Respect privacy and access permissions. Do not print private customer or behavioral event identifiers.

## Scope decision

1. **Existing conversion surface (page, form, checkout, campaign):** run a full evidence-led page and friction audit. Review mobile separately. Recommend specific fixes and any experiments.
2. **Offer being built, no live page yet:** run a *conversion-readiness preflight* on the approved offer and proposed buyer path. Examine audience, outcome, CTA, claims, cost/timing, proof availability, checkout effort and planned measurement. Mark page-level observations `NOT ASSESSED`; do not invent drop-offs or pretend a page was rendered.
3. **Offline/relationship-led offer without web conversion surface:** run a minimal handoff assessment, record `NOT APPLICABLE` for search/layout/form checks with reasons, and examine the next real buyer action. Do not impose a WordPress page or an A/B test.
4. **Focused standalone request:** perform only requested CRO work. No forced full-run task ledger or unrelated SEO implementation.

## Six gates (evaluate in order)

1. **Intent and relevance:** search query/ad/email/social promise -> destination headline, offer, FAQ and primary action. Do not invent query volumes. If SEO matters, inspect one H1, canonical, headings, relevant internal linking and visible answers; do not force SEO checks for non-search traffic.
2. **Value and offer accuracy:** WHAT, WHO, WHY, HOW above the fold; dream outcome, believable process, true time delay, effort/sacrifice, all material costs/eligibility/renewal/deposit/fulfilment conditions. No approval, funding, credit, savings, urgency or other outcome guarantees without evidence.
3. **Three-second test and attention:** one visual scan path (headline -> buyer benefit -> primary action -> succinct proof/terms). Check actual 320px and 390px mobile when rendered. Treat two competing CTAs, oversized nav and redundant cards as testable distraction hypotheses, not proven causes.
4. **Friction and behavior:** map observed Clarity/analytics actions and technical errors to stage, device, denominator and time window. Distinguish event counts from unique people and correlations from causes. Identify the earliest consequential barrier. Diagnose form validation, duplicate sign-in, field keyboard, slow submit, hidden CTA and state loss where evidence supports it.
5. **Trust and objections:** separate verified proof from inferred buyer concern. Name what is still unknown, and place real terms and relevant proof where the decision occurs. Never invent review excerpts, ratings, logos, bureau claims or a no-risk guarantee.
6. **Implementation/experiment readiness:** produce a minimal before/after recommendation with page region, precise copy/layout action, original elements to retain, technical dependencies, device QA and conversion measurement.

## Prioritization: fix before test

- **FIX FIRST** when an actual defect, broken path, misleading material fact, hidden required action, or incomplete feedback is confirmed. Repair for both experiment variants; establish a new baseline.
- **TEST** when the design/copy change is a plausible but unproven behavioral hypothesis. Define control/challenger, invariant backend, primary user-level metric, guardrails, assignment rules, consent/analytics boundaries and stopping or sample-size plan.
- **HOLD** if material legal/business facts, supporting evidence, live DOM, experiment separation, or accessibility cannot be established. A diagnostic may be useful while held; do not represent it as publication-ready.
- Use the **highest-consequence** observed barrier, not a pile of low-impact micro-edits.

## Deliverables

For a page audit, return `CRO_REVIEW.md` (or the requested equivalent) with:

1. **Evidence ledger:** source, observed/inferred/synthetic, time window, denominator, limitations.
2. **Offer/intent and six-gate assessment:** PASS/PARTIAL/FAIL/NOT ASSESSED or NOT APPLICABLE, with rationale.
3. **First barrier:** one primary problem and its evidence; up to three prioritized findings.
4. **Exact fix:** current -> proposed copy/layout/interaction, protected parts, owner decisions and engineering notes.
5. **Experiment:** only for unresolved hypotheses; control/B, what stays identical, primary metric, guardrails and sample plan.
6. **QA/release:** mobile 320/390, tablet 768, desktop 1440 *when an actual render is possible*; overflow, keyboard focus, body text >=16px mobile, contrast, functional submit, accessibility, source facts and approval holds.
7. **Downstream decision:** `FIX`, `TEST`, `READY FOR OWNER REVIEW`, `HELD` or `NOT APPLICABLE`, plus evidence gaps.

For a no-page offer preflight, use the same report but label unobserved page evidence `NOT ASSESSED`, propose a realistic conversion path, and identify the first test/implementation dependency. Do not claim screenshot QA.

When the owner requests implementation and actual source is available, provide a **separate** full working standalone HTML and a WordPress-compatible scoped variant if applicable; keep native theme header/footer and protected business logic untouched. Render and inspect 320, 390, 768, 1440px where tools permit. Do not substitute a demo for a live checkout. Never deploy, publish, send, or represent a conversion benefit as measured without a valid experiment.

## Full-offer waterfall integration

Follow `<plugin_root>/references/cro-waterfall.md`. For full multi-step offer runs, root performs the CRO readiness gate **after accepted offer/value/pricing and sales draft work, before final SUMMARY and checker**, even when CRO was not requested by name. The root owns `output/CRO_REVIEW.md`; do **not** introduce an unrecognized `sub-cro` task role, mode, new schema or phantom specialist execution.

Recommendations may loop back to the appropriate upstream offer, value, pricing or sales task **through root-controlled reconciliation** only. Owner approval is required for changes to commercial terms. Re-evaluate changed downstream artifacts and their hashes/reviews; never use the CRO gate to clear an existing business or independent-review hold. New sales-ready copy in a CRO artifact requires applicable high-risk classification and genuine separate-context review.

## Quality checks

- Clearly distinguish repaired UX from CRO experiments and their measured effects.
- Report `unknown` when data is missing; no qualitative heuristic score is a conversion metric.
- Preserve real terms and the original source. No generic stylistic rewrite may silently replace owner-approved words.
- `READY` from the structural checker is **not** commercial approval, independent review, or proof of conversion uplift.
