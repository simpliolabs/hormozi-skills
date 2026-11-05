# Orchestration Workflow (shared)

One workflow, loaded by both entry points: the `hormozi-orchestrator` skill (main conversation, Codex and skill-driven hosts) and `<plugin_root>/agents/hormozi-orchestrator.md` (Claude native). The owner talks to **one** chat. Specialists never interview the owner.

Original standalone skills in `<plugin_root>/skills/` stay the authority for methodology. Load a skill only when its task is selected. This file defines who decides, who writes, and in what order. It does not restate the frameworks.

## Authority

| Who | May | May not |
| --- | --- | --- |
| Root (the owner's chat) | Interview, route, freeze inputs, accept results, write `OFFER_DECISIONS.json`, `CLAIMS.json` status, `RUN_STATE.json`, compatibility outputs | Delegate a commercial decision |
| Specialist (`sub-*`) | Read its frozen inputs; write proposals and drafts to its assigned write set | Edit control files, approve terms, write outside its write set, read files not listed as inputs |

Decisions (price, currency, cadence, guarantee, eligibility, audience, scope) are root-only. A specialist proposing a change returns it as a proposal. An unauthorized state change holds that result. These are cooperative-agent contracts plus detection, not filesystem isolation.

## Workspace and state

Plugin files are read-only. Two roots: `plugin_root` (from the host-provided skill/agent base path) holds packaged references, contracts, skills and `scripts/check_outputs.py`; `workspace_root` (the invocation project) holds everything written. Hashes are root's job: children have Read/Write/Glob only, so root hashes inputs before dispatch and inputs plus outputs after return, and compares. Run QA as `python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <workspace_root>/output/runs/<run_id>`. All output goes to the **user's workspace**, never the plugin install cache. Use the invocation workspace's `output/`.

- Legacy deliverables keep their names: `output/<NAME>.md`.
- Control records: `output/runs/<run_id>/BRIEF.json`, `OFFER_DECISIONS.json`, `CLAIMS.json`, `RUN_STATE.json` (schemas in `<plugin_root>/contracts/`).
- `output/CHECKPOINT.md` and `output/QA_REPORT.md` are bound into `RUN_STATE.json` as `checkpoint` and `qa_receipt` (`path`, `sha256`, `decision_version`). An edited file or a newer decision version makes the receipt stale.
- Before replacing an artifact a prior run needs, keep the superseded copy once under `output/runs/<run_id>/artifacts/`.
- A file left over from another run is never an implicit input.

Phases: `INTAKE -> ROUTED -> DRAFTING -> RECONCILING -> NEEDS_APPROVAL -> SALES_ASSETS -> QA -> READY | HELD | FAILED`. READY means checked and ready for owner review. It never means published, deployed, legally approved, or commercially proven.

## Task contract

Every task in `RUN_STATE.json` declares `id`, `role`, optional `mode`, `depends_on`, `inputs` (path and sha256), and `write_set`.

1. **Frozen inputs.** A task reads only brief `sources` and the `write_set` of its declared dependencies, each frozen with a hash. Root hashes at dispatch. A changed input invalidates the task.
2. **Disjoint writes.** No two tasks share a write path.
3. **Not-run is explicit.** A skipped dependency is `not_requested` or `not_applicable`, never silently absent. Pricing gets a named offer version and audit/bonus inputs, or an explicit not-run status. It does not check whether a file happens to exist.
4. **Root accepts.** Root verifies hashes and versions before accepting a result, then updates the decision record.
5. **Repair limit.** If pricing changes scope or guarantee, root returns only the affected work for revision. After two failed repair passes, show the disagreement to the owner.

Modes are exact strings, and `scripts/check_outputs.py` enforces the order below: `proposal`, `audit`, `diagnostic`, `revision`, `revised_check`, `packaging_exploration`, `final_feasibility`, `copy`.

## Routes (original stages A-E)

| Stage | Order | Fixed inputs |
| --- | --- | --- |
| A Idea only | optional `sub-market` -> `sub-offer` (`proposal`) -> `sub-value` (`audit`) -> `sub-pricing` (`final_feasibility`) -> root reconciliation -> `sub-sales` | Brief only |
| B Offer exists, not converting | `sub-value` (`diagnostic`, writes `ORIGINAL_OFFER_AUDIT.md`) -> `sub-offer` (`revision`) -> `sub-value` (`revised_check`, writes `REVISED_OFFER_CHECK.md`) -> `sub-pricing` (`final_feasibility`) -> reconciliation -> `sub-sales` | The diagnostic reads the **frozen original**, whose hash is never overwritten |
| C Sales assets only | `sub-sales` only | Existing authorized offer version and claim check. No repricing, new guarantee, or market rebuild. Upstream tasks are `not_applicable` |
| D Service business, scale | `sub-pricing` (`packaging_exploration`, only if needed) -> `sub-offer` (`revision`) -> optional `sub-value` (`revised_check`) -> `sub-pricing` (`final_feasibility`) -> reconciliation -> `sub-sales` | Existing delivery and cost snapshot. Final economics always run after the last scope change |
| E Custom / mixed | The smallest dependency graph for the gaps found | A focused request runs one skill with proportionate QA |

### Automatic downstream CRO gate (new offer waterfall)

For **every full multi-step offer run** (stage A, B, D, or a comparable stage E offer workflow), perform a root-owned **CRO readiness gate after the accepted offer/value/pricing and requested sales drafts, before the final SUMMARY and output checker**, **even if the owner did not ask for CRO by name**. Stage C includes the gate when a landing page or another digital conversion destination is in scope. A focused one-skill request remains focused.

- Load the actual `<plugin_root>/skills/cro-page-optimizer/SKILL.md`, its `<plugin_root>/skills/cro-page-optimizer/references/CRO_FRAMEWORK.md`, and `<plugin_root>/references/cro-waterfall.md`. Do not infer CRO methodology from this paragraph.
- At route initialization, assign `CRO_REVIEW.md` to `BRIEF.requested_artifacts` and the **root** `write_set`, not an imaginary `sub-cro` role. For a page with genuine source and behavior data run full CRO; for an offer without a page run conversion readiness; for offline offers run a minimal buyer-handoff review with page and SEO marked not applicable. Missing source means NOT ASSESSED, not invented evidence or a false pass.
- Preserve task modes, role enums and existing schemas. Root writes `output/CRO_REVIEW.md`, records real hash, decision version, input provenance and any relevant QA findings, and carries its key decision into canonical `SUMMARY.md`. If publish-ready marketing wording appears in this artifact, classify it high-risk and apply the existing separate-context review floor.
- A CRO fix may propose an upstream revision, but root must obtain any required commercial approval before revising accepted offers, terms, or claims. Re-run affected downstream dependencies and revalidate artifact hashes/reviews. Do not use a CRO result to clear review or business holds.
- Explicit CRO-only requests select `cro-page-optimizer` directly. An individual request for five hooks does not trigger a whole offer waterfall.

Use `scripts/cro_gate.py` as a read-only eligibility/depth helper when Python is available, with the actual brief stage and evidenced conversion surface; its `depth` is not a `RUN_STATE.tasks[].mode`. If unavailable, apply the documented routing table and name the fallback. See `<plugin_root>/references/cro-waterfall.md` for the precise eligibility matrix, stage examples and invariant tests. This gate is a **method and root QA step**, not a newly supported `RUN_STATE.tasks[].mode` or a tested autonomous specialist invocation.

Rules that follow:

- `OFFER_AUDIT.md` is the normal audit name. In B it is the compatibility view of the latest revised audit. The original and revised audits stay separately named and have disjoint write sets.
- Do not require market research before editing a well-evidenced offer. Absence of research is an explicit condition, never a reason to invent it.
- `sub-sales` writes only the requested copy from authorized terms. It may not change price, guarantee, or scope.
- A focused request (for example "five hooks") returns exactly what was asked, with no full-run bookkeeping and no full output suite.

## Routing and effort

Record `requested_effort` and `observed_model` / `observed_effort` separately in `routing`. Use `unknown` when the runtime reports nothing. Never copy the request into the observation. Never substitute a costlier model silently. Requested defaults: `sub-market` medium, `sub-offer` high, `sub-value` medium, `sub-pricing` high, `sub-sales` medium. Escalate to high for conflicting evidence, failed offers, or high-risk copy.

## Method loading and delegation (required)

Structural `READY` from `check_outputs.py` is not proof that a method was applied. Before each selected task is drafted, its standalone method must actually be loaded: invoke the skill, or Read its `<plugin_root>/skills/<name>/SKILL.md` body and every reference that body names as required. Do not infer a method from the schemas, the checker source, or the role summaries in `<plugin_root>/agents/sub-*.md`, and do not shape output to pass the checker instead of the method.

- **Delegated task:** give the worker the exact packaged `<plugin_root>/skills/<name>/SKILL.md` path (and its required references) in the native dispatch's allowed-read list as read-only instruction context, and require the worker to read it before drafting. Packaged methods, required references and `sub-*.md` role instructions are instruction context only: never list them in `RUN_STATE.tasks[].inputs` or `BRIEF.sources`, which hold workspace business data only (the frozen, hash-checked task inputs). Use the host's observed native subagent tool (`Agent`; legacy hosts may call it `Task`). Never name a tool the runtime did not show.
- **Root fallback:** root may run the task itself only when native dispatch is unavailable or refused, never silently because it is convenient. Record the exact reason (tool absent, or the refusal text) in the owner summary or QA note. Root then loads the same skill body itself.
- **Report what was loaded.** The owner summary or QA note names, per selected task, the skill and references actually loaded, or `not loaded` / `unknown` when the runtime did not show it. This is a statement in the report, not a new schema, ledger or instrumentation.

## Evidence and QA

A clean ledger does not prove clean copy. Semantic review inspects each final artifact and binds its receipt to the artifact hash and decision version.

**Independent-review floor (required).** In a controlled run, every manifest artifact produced by a `sub-sales` task, the canonical `output/PITCH.md`, `output/HOOKS.md` and `output/LANDING_PAGE.md` (whoever produced them, any safe path spelling), and any artifact marked `high_risk: true` needs a passing review with `context: "separate"` bound to its exact path, hash and decision version. There are no bookkeeping or filename exclusions; renaming a sales output does not remove the requirement. Set `high_risk: true` on those artifacts yourself, but the checker applies the floor even when the flag is false or absent, `ready` is false or the phase is `HELD`. A same-context or missing review is not independent approval: never record same-context work as `separate`, never invent a reviewer run, and never copy a model request into an observation. If a separate reviewer is unavailable or refused, record the exact reason and fall back honestly to your own same-context review, which leaves the hold open.

While any required independent review is missing, add exactly this blocker to `RUN_STATE.blockers`: `[review] Independent review remains required.`, finish with phase `HELD`, and write every unresolved review obligation (artifact path and reason) into both `output/CHECKPOINT.md` and `output/QA_REPORT.md` so the three records agree. The checker never clears or edits it; remove the blocker yourself only after real separate-context passes exist. Held drafts stay useful: still deliver the full provisional result and `SUMMARY.md`.

**Declared business limitation.** During semantic intake, after reading the actual sources and before freezing or delegating the brief, decide whether the known fictional-fixture / no-real-validation limitation applies. If it does, declare it yourself as the exact string `Fictional fixture; real business validation absent` in `BRIEF.constraints`, register the identical string in `RUN_STATE.blockers`, and name it as an unresolved business hold in both `output/CHECKPOINT.md` and `output/QA_REPORT.md`. The marker is your semantic judgment, never implied by source types or wording; other real-business limitations still need honest registration in your own words. In ready validation the checker only requires a declared marker to be registered as the identical blocker (it derives the hold and `BUSINESS_VALIDATION_BLOCKER_UNREGISTERED` if not); it never infers, writes or clears it. A missing declaration is a semantic acceptance failure the checker cannot see. A genuine independent review resolves only its own copy-review hold, not this one; remove the blocker yourself only when real business validation exists.

Check with `python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <workspace_root>/output/runs/<run_id> --mode ready`.

## Checkpoint, resume and the final owner response (required)

- **Persist before delegating.** Write the initial `RUN_STATE.json` (phase `ROUTED`, declared tasks) and `output/CHECKPOINT.md` (route, decisions so far, next step) before the first delegation. After each accepted task, update both. If the work is interrupted, read that checkpoint and resume in the **same conversation**; do not start a second run or a second chat.
- **The chat reply is the deliverable.** The final owner response carries the substantive compact draft result itself, not only artifact paths or internal records: the offer in plain words, the Value Equation reasoning (dream outcome, perceived likelihood, time delay, effort and sacrifice, one line each), the decisions and who approved them, and the cheapest validation next steps to run before spending money. Unknown terms and QA holds are named honestly and the result is labelled a draft, but they never suppress the useful provisional result. A sparse idea still gets this reply.
- **The canonical owner summary is `output/SUMMARY.md` (required for full runs).** A full run is stage A, B or D; two or more active specialist tasks; more than one requested business deliverable; or an explicit summary request. Put `SUMMARY.md` in the initial requested artifacts and the root task's write set, write it from the accepted artifacts, and declare it in the manifest with hash, decision version and review like any other artifact. An alias such as `OWNER_SUMMARY.md` or a nested file never stands in for it, and a focused one-deliverable run does not need it. Use exactly these level-two headings, each once and non-empty: `## Offer`, `## Key Decisions`, `## Best Hook`, `## Next Actions`. Best Hook states the chosen hook itself (a quotation or paragraph), never only a path or link to `HOOKS.md`. Next Actions is exactly three prioritized, substantive top-level items numbered `1.`, `2.`, `3.` (the action text sits on the marker line, markers share one 0-3 space indent, and wrapped or nested explanation beneath is fine; a separate paragraph never fills an empty item). Honest unknowns and holds belong in Key Decisions. The checker verifies this structure only; whether the hook is the right one and the actions are good stays with the semantic review.
- **Authoring uses the contract, not the checker's source.** Build records from `<plugin_root>/contracts/` schemas and this reference, then invoke the checker. Read checker source only to diagnose a concrete failed tool or config error.
