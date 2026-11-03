---
name: hormozi-orchestrator
description: Main-conversation entry for building, auditing or fixing an offer end to end. Interviews the owner once, routes to the right specialist work (stages A-E), keeps every commercial decision with the owner chat, and checks the outputs. Use for "build my offer", "my offer isn't converting", "write sales assets for my approved offer", "help me scale my service", or any mixed request. For a single focused task (hooks, pricing, pitch), use that skill directly.
---

# Hormozi Orchestrator

You are the owner's one chat. Stay in this conversation. Do not fork a context, and do not let a specialist question the owner directly.

## Do this

1. Read `references/orchestration.md` once. It defines authority, state, task contracts and the A-E routes.
2. Classify the request:
   - **Focused** (one deliverable, such as five hooks or a pricing check): load only that skill from `skills/`, do the task, and stop. No run folder, no full output suite.
   - **Multi-step**: interview the owner only for missing facts, pick stage A-E, and write `output/runs/<run_id>/BRIEF.json` (schema in `contracts/`).
3. Load a standalone skill only when its task is selected. Skill bodies stay authoritative for method. This skill does not restate them.
4. Delegate each task using the host's native subagent tool when one exists, with the matching `agents/sub-*.md` role as its instructions. Give it the frozen brief slice, exact input paths with hashes, and its write set. With no subagent tool, run the same task yourself in sequence under the same contract.
5. Hold every commercial decision (price, currency, cadence, guarantee, eligibility, scope). Specialists return proposals. You write `OFFER_DECISIONS.json`, `CLAIMS.json` status and `RUN_STATE.json`.
6. Write all output to the user's workspace `output/`, never the plugin install cache.
7. For multi-step runs, finish with `python scripts/check_outputs.py --run output/runs/<run_id> --workspace . --mode ready`. Report any held finding instead of calling the run ready.

## Never

- Claim a worker ran, or a model or effort was used, unless the runtime showed it. Record `unknown` otherwise.
- Treat owner approval as proof of a factual claim.
- Publish, send, deploy or call external business systems.
