# Approved Architecture (v1.1.0)

One owner chat, five logical specialists, root-owned commercial decisions. Source of truth for the approved design is `APPROVAL_PLAN_v3.md` (sections 3-9); this file records what shipped.

## Entry points
- `skills/hormozi-orchestrator/SKILL.md` (Codex, skill-driven hosts) and `agents/hormozi-orchestrator.md` (Claude native) load the single workflow in `references/orchestration.md`. Neither forks a context.
- The 17 business skills stay standalone. A focused request loads one skill, with no run folder.

## Two roots
- `plugin_root`: read-only packaged content, derived from the host-provided skill or agent base path (`<plugin_root>/skills/<name>/`). Holds `references/`, `contracts/`, `skills/`, `agents/`, `scripts/check_outputs.py`.
- `workspace_root`: the invocation project. All output and run records are written here, never to the plugin cache.
- QA: `python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <workspace_root>/output/runs/<id>`.

## Authority
- Root alone writes `OFFER_DECISIONS.json`, `CLAIMS.json` status and `RUN_STATE.json`. Specialists return proposals.
- Children have Read/Write/Glob only and cannot calculate hashes. Root hashes inputs before dispatch and inputs plus outputs after return, and compares. A child never reports a hash.

## Deterministic checks (`scripts/check_outputs.py`)
- Money: every bound money field is checked against its structured value (amount, currency, cadence), with or without an optional `display`. A money-shaped value must declare `kind: money`. Unrelated example amounts in prose are not mistaken for the selling price.
- Guarantee `conditions` must appear in the rendered terms.
- Ready mode holds on open blockers, unfinished tasks and incomplete artifact producers.
- BRIEF, OFFER_DECISIONS and RUN_STATE must agree on `run_id` and `offer_id`.
- Requested artifacts match by exact path (`PITCH.md` means `output/PITCH.md`), not basename.
- A clean check never proves clean prose; semantic review bound to artifact hash and decision version remains required.

## Runtime roles
| Role | Requested effort |
| --- | --- |
| `sub-offer`, `sub-pricing`, adversary | high |
| `sub-market`, `sub-value`, `sub-sales` | medium |

Claude agents keep their `sonnet` baseline. `.codex/agents/*.toml` and `.codex/config.toml` (concurrency 3) are optional, request effort only, omit model IDs, and apply to a trusted checkout of this repository. They do not register roles for an installed plugin. Requested and observed routing are recorded separately; `unknown` when the runtime shows nothing.
