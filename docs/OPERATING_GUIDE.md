# First-use operator guide

This guide applies to the Simpliolabs fork of Hormozi Skills at a specifically recorded Git commit. It describes **supervised use**, not commercial release.

## 1. Install the intended revision

1. Clone `https://github.com/simpliolabs/hormozi-skills.git` (or register that fork as the Claude marketplace).
2. Record the exact installed commit with `git rev-parse HEAD`. For the initial merged review baseline, the known merge commit is `b05b1c041b27b2fbf5bc4225ff14c48abaf40e2f`.
3. Confirm that `skills/hormozi-orchestrator/SKILL.md`, `references/orchestration.md`, `contracts/` and `scripts/check_outputs.py` resolve from the *same* installed root.
4. Confirm how your host actually loads the skill and whether specialist delegation is available. Do not treat a role definition as proof that a distinct agent executed.
5. For a focused request, invoke only the relevant standalone skill. Full orchestration and run controls are not required for every focused task.

## 2. Choose a lightweight entry

For a beginner, start with [Start Here](START_HERE.md): "I have a business idea and don't know where to start. Ask me one question at a time."

For an experienced user, request the exact deliverable, for example "Write five hooks for this approved offer." That route loads **one skill**, not the full offer pipeline. See [Adaptive routing](../references/adaptive-routing.md) for QUICK / GUIDED / opt-in DEEP behavior, progressive instruction loading, frozen briefs and checkpoint reuse. The policy is a resource discipline, **not** a measured or hard token cap.

If the request is a full multi-stage offer workflow, the downstream CRO gate remains part of the accepted path. A narrow focused request does not trigger the full waterfall.

## 2. Activate the guided experience

After installation in a compatible host, begin with this plain-language request:

> Help me build a stronger business offer. Guide me through the process one question at a time, then help with the offer, positioning, pricing, hooks, and landing-page draft. Clearly label what still needs my approval.

The existing orchestrator skill description is already scoped to multi-step offer creation or repair. Automatic activation depends on the host and installed skill discovery. When it does not activate, select the skill explicitly:

- **Claude Code:** Use `/` to open available commands/skills and find the installed orchestrator.
- **Codex:** Select the skill using `/skills` or mention `$hormozi-orchestrator` if installed.
- **ChatGPT:** Use the `@` skill selector if this skill is available in your skill library.

A short `/offer` alias is a **proposed follow-up**, not a currently implemented command in this fork. It would require compatibility testing and separate review; do not instruct users to rely on it yet.

## 3. Start a supervised, non-public pilot

Provide a brief with customer, offer, source-backed claims, known unknowns and owner-controlled decisions. Do not invent market validation, guarantees, pricing approvals, reviewers or receipts.

Suggested pilot prompt:

> Use the installed `hormozi-orchestrator` to audit this **internal draft** offer. Use only the facts and sources I provide. Label unverified claims and unresolved commercial decisions. Record actual specialist dispatch or fallback as observed. Produce the prescribed summary and controls. Do not publish, send, deploy, or take external business-system actions.

Avoid actual customer secrets or confidential personal data in a public demonstration.

### CRO is called for in the full offer waterfall

The V1 instructions call for a **downstream CRO readiness gate** in a full new-offer or offer-repair run even if the request never says CRO. After offer, value, pricing and requested sales work, they direct the root to load `cro-page-optimizer` and record `output/CRO_REVIEW.md`.

- For an existing page, provide actual URL/HTML or screenshots and analytics to permit a concrete mobile/form/intent audit. Missing information is `NOT ASSESSED`.
- For a new offer with no page, the skill examines conversion readiness, not imaginary webpage metrics.
- For an offline offer, the skill checks real buyer handoff and marks irrelevant search/form checks `NOT APPLICABLE`.
- A root-owned CRO gate does **not** create a new agent, task mode or claim that a separate reviewer executed. Existing review/business holds survive.
- A standalone focused request, such as five hooks, remains focused.

Optional deterministic planning example: `python scripts/cro_gate.py --stage A --surface planned`. This helper prints the required gate/depth as JSON. It never writes records or changes authorization.

V1 eligibility is an instruction-level root obligation, demonstrated in one fresh full-offer native run. The checker cannot detect an eligible run if root omits CRO from the brief entirely; in ready mode with valid brief and run state records, existing manifest and file checks require `CRO_REVIEW.md` once declared in `BRIEF.requested_artifacts`. The helper defaults Stage E to offer work, so pass `--no-offer-workflow` for unrelated custom work. These routing instructions are not a hard token cap: the corrected full-offer run used more tokens and time than the original. Native differentiated specialist dispatch was refused, and native browser-render QA remains unproven.

## 4. Inspect outputs and checks

For controlled multi-step work, look for:

- `output/SUMMARY.md` with `## Offer`, `## Key Decisions`, `## Best Hook` (the chosen hook text) and `## Next Actions` (three prioritized actions).
- `output/CHECKPOINT.md`, `output/QA_REPORT.md`, run state, claim/decision records, and the manifest.
- Results from `python scripts/check_outputs.py --workspace <workspace-root> --run <workspace-root>/output/runs/<run-id> --mode ready` (from the corresponding installed root; consult the checked-in scripts and docs for host-specific details).

Controlled sales outputs have a review floor even if their `high_risk` metadata is false or absent. Missing, failed, stale or same-context evidence must remain a hold, together with one aggregate review blocker where required. A checker is not an independent reviewer, and a receipt is cooperative metadata rather than cryptographically authenticated proof.

For controlled priced offers, normal Stage A/B/D runs include final feasibility. In ready mode, the read-only checker derives **two distinct holds** from `OFFER_DECISIONS`: unresolved refund/cancellation terms and unverified delivery costs/financial feasibility. An `unknown` or `proposed` value is not approved; a generic blocker or existing `HELD` phase does not hide either obligation. The same floor applies at any stage with a requested or manifested `output/PRICING.md` or active final-feasibility task. Stage C/E work without that pricing scope is outside this floor. Evidence and authorization references are cooperative records, not independent proof that a business decision was approved or profitable.

## 5. Decide what is ready

`READY` means checker-defined **structural** conditions are satisfied. It is **not** factual validation, independent business advice, permission to make commercial claims, or authority to publish.

`HELD` means unresolved obligations must remain visible to the owner. Drafts can still be useful, but they are not cleared for commercial release.

The recorded [seven-obligation acceptance](SEVEN_HOLD_VALIDATION.md) verifies preservation in one bounded fictional workflow. It does not establish universal detection of undeclared business limitations or authenticated separate-context execution. The observed native attempt fell back sequentially after a refused diagnostic dispatch.

## 6. Safe next milestones

- Have a human owner check prices, guarantees, eligibility, claims and source evidence.
- Document which methods and agents actually ran in the target host.
- Independently test reviewer provenance/dispatch before claiming trustworthy automation.
- Keep release, deployment and publication behind distinct approvals.
