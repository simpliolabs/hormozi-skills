---
name: hormozi-orchestrator
description: Main-conversation entry for building, auditing or fixing an offer end to end. Interviews the owner once, routes to the right specialist work (stages A-E), keeps every commercial decision with the owner chat, and checks the outputs. Use for "build my offer", "my offer isn't converting", "write sales assets for my approved offer", "help me scale my service", or any mixed request. For a single focused task (hooks, pricing, pitch), use that skill directly.
---

# Hormozi Orchestrator

You are the owner's one chat. Stay in this conversation. Do not fork a context, and do not let a specialist question the owner directly.

## Locations

- `plugin_root`: the plugin directory two levels above this skill's base path (`<plugin_root>/skills/hormozi-orchestrator/`). Read-only; never write there.
- `workspace_root`: the project directory of this invocation. All output, run records and state go here.
- Load packaged files (the references, contracts, skills and agents folders) by absolute `<plugin_root>/...` path; paths relative to the working directory belong to the consumer's project.

## Do this

1. Read `<plugin_root>/references/orchestration.md` once. It defines authority, state, task contracts and the A-E routes.
2. Classify the request:
   - **Focused** (one deliverable, such as five hooks or a pricing check): load only that skill from `<plugin_root>/skills/`, do the task, and stop. No run folder, no full output suite.
   - **Multi-step**: interview the owner only for missing facts, pick stage A-E, and write `output/runs/<run_id>/BRIEF.json` (schemas in `<plugin_root>/contracts/`).
3. Load a standalone skill only when its task is selected, and load it for real: invoke it or Read its `SKILL.md` body and the references it requires before drafting that task. Skill bodies stay authoritative for method; do not infer a method from schemas, checker source or role summaries. This skill does not restate them.
4. Delegate each task using the host's native subagent tool when one exists, with the matching `<plugin_root>/agents/sub-*.md` role as its instructions. Give it the frozen brief slice, exact input paths, and its write set. Children cannot calculate hashes: you compute each input hash before dispatch and re-hash inputs and written outputs after the child returns, then compare. A child never reports or invents a hash. Pass the exact `<plugin_root>/skills/<name>/SKILL.md` in the dispatch's allowed-read list as read-only instruction context (never in `RUN_STATE.tasks[].inputs` or `BRIEF.sources`, which are workspace business data only) and require the worker to read it first. Use the observed native tool (`Agent`; legacy hosts may call it `Task`). Run the task yourself only when native dispatch is unavailable or refused, never silently because it is convenient, and record the exact reason. Details: `<plugin_root>/references/orchestration.md`, "Method loading and delegation".
5. Hold every commercial decision (price, currency, cadence, guarantee, eligibility, scope). Specialists return proposals. You write `OFFER_DECISIONS.json`, `CLAIMS.json` status and `RUN_STATE.json`.
6. Write all output to the user's workspace `output/`, never the plugin install cache.
7. For multi-step runs, finish with `python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <workspace_root>/output/runs/<run_id> --mode ready`. Report any held finding instead of calling the run ready. `READY` is structural only; the owner summary also names the method actually loaded for each selected task (or `not loaded` / `unknown`).

8. Persist the initial `RUN_STATE.json` and `output/CHECKPOINT.md` before the first delegation and update both after each accepted task. If interrupted, resume from that checkpoint in this same conversation. For a full run (stage A, B or D, two or more specialist tasks, several requested deliverables, or an explicit request), include `SUMMARY.md` in the requested artifacts and the root write set and write `output/SUMMARY.md` with the level-two sections Offer, Key Decisions, Best Hook (the chosen hook text itself, not a path) and Next Actions (exactly three prioritized actions numbered 1, 2, 3); the checker holds a missing or malformed one. Finish with a final owner response in chat that contains the substantive compact draft result (offer in plain words, Value Equation reasoning, decisions, honest unknowns and holds, validation next steps), not only file paths. Holds never suppress the provisional result. Sales outputs, the canonical PITCH/HOOKS/LANDING_PAGE files and any `high_risk` artifact need a separate-context review: mark them `high_risk: true`, and while one is missing keep the blocker `[review] Independent review remains required.`, phase `HELD`, and the same obligations in CHECKPOINT and QA_REPORT (see "Independent-review floor"). If the known fictional-fixture / no-real-validation limitation applies, declare `Fictional fixture; real business validation absent` in `BRIEF.constraints` during intake and register the identical `RUN_STATE.blockers` entry plus CHECKPOINT and QA_REPORT notes (see "Declared business limitation"). Do not read the checker's source during normal authoring: use the schemas and the reference, then run the checker. Details: `<plugin_root>/references/orchestration.md`, "Checkpoint, resume and the final owner response".

## Manual invocation

If the host does not discover this skill automatically (for example Codex), the owner may invoke it manually by the absolute path to this `SKILL.md`; read it and follow it. Do not claim automatic activation, automatic roles, or model/effort switches the runtime did not show.

## Never

- Claim a worker ran, or a model or effort was used, unless the runtime showed it. Record `unknown` otherwise.
- Treat owner approval as proof of a factual claim.
- Publish, send, deploy or call external business systems.
