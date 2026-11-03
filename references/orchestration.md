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

Rules that follow:

- `OFFER_AUDIT.md` is the normal audit name. In B it is the compatibility view of the latest revised audit. The original and revised audits stay separately named and have disjoint write sets.
- Do not require market research before editing a well-evidenced offer. Absence of research is an explicit condition, never a reason to invent it.
- `sub-sales` writes only the requested copy from authorized terms. It may not change price, guarantee, or scope.
- A focused request (for example "five hooks") returns exactly what was asked, with no full-run bookkeeping and no full output suite.

## Routing and effort

Record `requested_effort` and `observed_model` / `observed_effort` separately in `routing`. Use `unknown` when the runtime reports nothing. Never copy the request into the observation. Never substitute a costlier model silently. Requested defaults: `sub-market` medium, `sub-offer` high, `sub-value` medium, `sub-pricing` high, `sub-sales` medium. Escalate to high for conflicting evidence, failed offers, or high-risk copy.

## Method loading and delegation (required)

Structural `READY` from `check_outputs.py` is not proof that a method was applied. Before each selected task is drafted, its standalone method must actually be loaded: invoke the skill, or Read its `<plugin_root>/skills/<name>/SKILL.md` body and every reference that body names as required. Do not infer a method from the schemas, the checker source, or the role summaries in `<plugin_root>/agents/sub-*.md`, and do not shape output to pass the checker instead of the method.

- **Delegated task:** give the worker the exact packaged `<plugin_root>/skills/<name>/SKILL.md` path (and its required references) as an allowed input, and require the worker to read it before drafting. Use the host's observed native subagent tool (`Agent`; legacy hosts may call it `Task`). Never name a tool the runtime did not show.
- **Root fallback:** root may run the task itself only when native dispatch is unavailable or refused, never silently because it is convenient. Record the exact reason (tool absent, or the refusal text) in the owner summary or QA note. Root then loads the same skill body itself.
- **Report what was loaded.** The owner summary or QA note names, per selected task, the skill and references actually loaded, or `not loaded` / `unknown` when the runtime did not show it. This is a statement in the report, not a new schema, ledger or instrumentation.

## Evidence and QA

A clean ledger does not prove clean copy. Semantic review inspects each final artifact and binds its receipt to the artifact hash and decision version. High-risk readiness needs a separate-context reviewer, or it is held.

Check with `python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <workspace_root>/output/runs/<run_id> --mode ready`.
