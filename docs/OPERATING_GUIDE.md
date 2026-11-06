# First-use operator guide

This guide applies to the Simpliolabs fork of Hormozi Skills at a specifically recorded Git commit. It describes **supervised use**, not commercial release.

## 1. Install the intended revision

1. Clone `https://github.com/simpliolabs/hormozi-skills.git` (or register that fork as the Claude marketplace).
2. Record the exact installed commit with `git rev-parse HEAD`. For the initial merged review baseline, the known merge commit is `b05b1c041b27b2fbf5bc4225ff14c48abaf40e2f`.
3. Confirm that `skills/hormozi-orchestrator/SKILL.md`, `references/orchestration.md`, `contracts/` and `scripts/check_outputs.py` resolve from the *same* installed root.
4. Confirm how your host actually loads the skill and whether specialist delegation is available. Do not treat a role definition as proof that a distinct agent executed.
5. For a focused request, invoke only the relevant standalone skill. Full orchestration and run controls are not required for every focused task.

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

## 4. Inspect outputs and checks

For controlled multi-step work, look for:

- `output/SUMMARY.md` with `## Offer`, `## Key Decisions`, `## Best Hook` (the chosen hook text) and `## Next Actions` (three prioritized actions).
- `output/CHECKPOINT.md`, `output/QA_REPORT.md`, run state, claim/decision records, and the manifest.
- Results from `python scripts/check_outputs.py --workspace <workspace-root> --run <workspace-root>/output/runs/<run-id> --mode ready` (from the corresponding installed root; consult the checked-in scripts and docs for host-specific details).

Controlled sales outputs have a review floor even if their `high_risk` metadata is false or absent. Missing, failed, stale or same-context evidence must remain a hold, together with one aggregate review blocker where required. A checker is not an independent reviewer, and a receipt is cooperative metadata rather than cryptographically authenticated proof.

## 5. Decide what is ready

`READY` means checker-defined **structural** conditions are satisfied. It is **not** factual validation, independent business advice, permission to make commercial claims, or authority to publish.

`HELD` means unresolved obligations must remain visible to the owner. Drafts can still be useful, but they are not cleared for commercial release.

The recorded [seven-obligation acceptance](SEVEN_HOLD_VALIDATION.md) verifies preservation in one bounded fictional workflow. It does not establish universal detection of undeclared business limitations or authenticated separate-context execution. The observed native attempt fell back sequentially after a refused diagnostic dispatch.

## 6. Safe next milestones

- Have a human owner check prices, guarantees, eligibility, claims and source evidence.
- Document which methods and agents actually ran in the target host.
- Independently test reviewer provenance/dispatch before claiming trustworthy automation.
- Keep release, deployment and publication behind distinct approvals.
