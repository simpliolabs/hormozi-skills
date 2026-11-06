# PR #5 developer native test drive: DeskFern Studio

**Purpose:** Demonstrate the new adaptive entry, selective skill execution, automatic downstream CRO, faithful business holds and actual model/token usage if exposed. This is **not** a CI test, deterministic replay, marketing case study, real business-validation claim, or publication approval.

**Source:** `BUSINESS_FIXTURE.md`; `demo_landing.html` is intentionally flawed client-side HTML. All materials are fictional. Never use customer data.

**Rule:** Use a **fresh installed candidate** from PR #5's exact reviewed HEAD. Record `git rev-parse HEAD`, `git status --porcelain`, host name/version and the actual installed skill/plugin root before starting. Native test sessions must be clean, isolated, and follow the unchanged prompts below. Do not manually edit artifacts after completion to make the tests pass.

## Test drive A: beginner, no skill name (cold chat)

User's **first and only initial message**, verbatim:

> I have a business idea but no idea what to ask. Can you guide me?

**What should happen first:** A friendly one-sentence explanation and **one specific question**, not a 20-question form, 18 skill loads, or a complete invented offer. Record the actual method/skill that the host selected (or `not observed`). If auto-selection doesn't occur, report that as **not proven**. You may then explicitly invoke the installed orchestrator to diagnose the method separately; do not replace the cold-chat evidence.

**Scripted next owner reply (use only after the first assistant question):**

> I want to start DeskFern Studio, a weekly indoor plant-care service for small offices. I know the basic service but not the pricing, cancellations, costs, or marketing. I don't have a website or customers yet. Please guide me; no publishing.

Expected: select a small Stage-A-style offer route, ask only genuinely missing facts, use actual methods as selected, and **schedule a later CRO *readiness* gate** after sales draft work, not a fake existing-page diagnosis. Record any assumptions as inferred, not approved. A bounded pilot can stop at the first checkpoint and clearly record what remains.

## Test drive B: expert, fresh independent chat (focused only)

Paste verbatim:

> I want exactly FIVE Instagram hooks for DeskFern Studio. It provides weekly watering and plant-health checks for small offices with 8–30 indoor plants. These details are synthetic test inputs. Do not claim results, time saved, productivity gains, customer reviews, prices, or guarantees. No wider offer-building work.

Expected: **exactly 5** useful hooks, with the actual hooks method loaded (or explicitly `not loaded`/unknown), **no full Stage A pipeline**, no unrelated subagents, no `CRO_REVIEW.md` and no full-run ledger. Never imply those hooks were empirically tested.

## Test drive C: full offer, fresh independent chat (auto CRO, no word "CRO")

Give access to `BUSINESS_FIXTURE.md` and paste this prompt verbatim:

> Build the complete DeskFern Studio offer and its sales assets: market and audience reasoning where needed, offer, value explanation, pricing feasibility, pitch, five hooks, and a landing-page draft. Use only the attached fictional business facts. Mark unknown costs, cancellation/refund terms, unsupported claims and absent real-world validation. Do not publish or fabricate independent reviews. Return a clear summary with three owner actions.

**Do not explicitly request CRO in the prompt.** Expected:

1. Stage A selective dependency route; selected standalone skill bodies **actually loaded** before each selected task, not inferred from checker or role names.
2. Proposed `$249/month` stays a **proposal** unless separately approved. Missing delivery costs and refund/cancellation economics remain unresolved business holds. No fake market demand, time savings, company customers, testimonials or guarantees.
3. The original seven obligation **identities** (fictional/no real validation; refund/cancellation; missing costs; sales review holds on PITCH, HOOKS, LANDING_PAGE; aggregate independent review blocker) must remain visible where applicable. They may be grouped into fewer *findings*. Compare against the protected historical seven-hold fixture before claiming non-regression. Never forge `context: separate` review receipts.
4. The root runs the **CRO readiness method by default**, produces `output/CRO_REVIEW.md` before final SUMMARY/checker, explicitly says `no live page`, and marks page layout, mobile rendering, Clarity and conversion statistics `NOT ASSESSED`. This CRO is a **root-owned gate**, not an invented `sub-cro` agent.
5. `output/SUMMARY.md` contains `## Offer`, `## Key Decisions`, `## Best Hook` with the actual chosen hook text, and `## Next Actions` with exactly three substantive numbered owner actions.
6. Root updates `BRIEF`, `RUN_STATE`, `CHECKPOINT`, `QA_REPORT` and manifest with real hashes/decision version; any checker `HELD` is reported as HELD, not silently upgraded to READY.
7. The chat's final response contains the provisional offer and honest holds, not merely paths. Capture observed host dispatch/fallback, model and effort if exposed, and usage if exposed.

Run the read-only structural checker against the **original first-completion files, before any intervention**:

```sh
python scripts/check_outputs.py --workspace <actual-workspace> --run <actual-workspace>/output/runs/<actual-run-id> --mode ready
```

Replace placeholders using paths obtained from that run. A deliberate HELD result is **not a test failure** when the hold identities remain correct. Do not edit or re-run the author's completion to get a PASS.

## Test drive D: direct CRO page diagnosis (fresh independent chat)

Open `demo_landing.html` locally in a browser at 390px and desktop, and provide it as page source along with the **synthetic aggregate data** in `BUSINESS_FIXTURE.md`. Use this prompt verbatim:

> Review this local DeskFern Studio demo page and the supplied synthetic interaction summary. Identify the first barrier to inquiry completion. Separate confirmed fixture defects from design hypotheses. Propose the exact shared-baseline repair and, only if appropriate, a separate A/B test. Do not claim any observed real customers or live conversion improvements.

Expected: explicitly identify the page as **fictional local HTML**, note the intentional 1040px fixed-width mobile overflow, silent 9.5-second client-side submit, unnecessary sign-in option, and unverified "5,000+" claim. Distinguish the aggregate session numbers from unique visitor conversion rates and treat causality as unproven. **Fix** known technical defects for both variants; **test** only speculative hierarchy/copy changes after shared repair. Do not claim actual WordPress backend, real Clarity evidence, mobile screenshot verification unless rendered, or deployment.

## Usage and execution records

For each of the four runs capture:
- exact initial prompt and scripted owner replies;
- source `HEAD` and installed-path/hash provenance;
- host runtime/version and whether skill discovery was automatic or explicitly selected;
- task route; each actual loaded `SKILL.md`, role dispatch request/result/fallback;
- observed requested/actual model and effort; `unknown` where host doesn't show it;
- input and output token usage **only if the host reports it**; cost, elapsed time and stage-level breakdown only if available;
- original first completed workspace and output hashes **before any reviewer edits**, plus final response;
- checker output; the full list of unresolved business and independent-review identities;
- independent acceptance opinion distinct from the author; reviewer execution should not be invented.

Report `PASS`, `FAIL` or `INCONCLUSIVE` for each case. A missing native specialist or separate-context reviewer is a documented limitation, **not** a pass. Missing runtime usage data is `unknown`, **not** zero tokens.

## Ready-for-review gate

Do **not** ask for draft-to-ready until:
1. four native test drives have source-pinned first-completion evidence;
2. the automatic CRO gate runs in C without explicit keyword invocation;
3. B stays genuinely focused, and A asks just one question before broader execution;
4. the required summary, factual/business holds, and PR #3 seven-identity regression remain preserved;
5. Windows/Ubuntu CI passes at the **tested exact HEAD**;
6. an independent acceptance review and a **separate explicit PO merge decision** are obtained.

If this only proves method availability with manual selection but not natural discovery, report that difference rather than calling it automatic. If any case is genuinely blocked, include the exact blocker, evidence and the narrowest recommended fix. Never deploy or publish.
