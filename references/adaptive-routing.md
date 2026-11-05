# Adaptive routing: beginner guidance, expert focus, economical runs

Normative for existing `hormozi-orchestrator` entrypoints. Supplement `<plugin_root>/references/orchestration.md` and `<plugin_root>/references/cro-waterfall.md`. Do not introduce a new role, mode, phase, schema, model switch or untested slash alias.

## Two paths, one entrypoint

- **GUIDED:** For "I have a business idea", "help me build an offer", "my offer isn't working", or "I don't know where to start", reflect the known goal and ask **one essential question at a time**, with an example answer. Classify A-E only after enough context. Do not show users role names, ledgers or all skill names unless requested. Do not interrogate them with a questionnaire.
- **FOCUSED:** For "write five hooks", "audit this pricing", "draft a pitch", or "diagnose my checkout", load **only the relevant standalone skill and its required references**; return the requested quantity. Apply its common evidence/authority preflight but do not create a full run or force upstream offer/CRO work. For explicit CRO, use `cro-page-optimizer` directly.
- **DEEP:** On explicit request for a comprehensive research/competitor/design/implementation scope, present the added tasks and dependencies before expanding. Never claim an automatic budget cap.

Natural language matching depends on the installed host. If the skill does not activate, use its explicit skill selector. `/offer` is not a working alias in this repo until separately implemented and tested.

## The smallest sufficient waterfall

| Goal | Selected work |
|---|---|
| Stage A complete new offer | Optional market -> offer -> value -> final pricing -> owner decisions -> requested sales -> root CRO readiness -> SUMMARY/checker |
| Stage B underperforming existing offer | Frozen original diagnostic -> needed revision -> revised check -> final feasibility -> requested sales -> root CRO gate -> SUMMARY/checker |
| Stage D scaling offer | Affected packaging/offer/pricing work -> authorized sales -> root CRO or offline handoff |
| Stage C sales assets only | Sales skill; root CRO gate only if a digital conversion destination is in scope |
| Stage E custom | Minimal dependency graph; root CRO only for multi-step **offer** workflows |
| One skill task | Single method, no full waterfall |

The full CRO gate is default in eligible multi-step **offer** runs even if not named; offline and no-page cases receive proportionate readiness/handoff, not fictional screenshots. **All standalone skills retain their evidence and owner-approval rules**, but they do not each trigger every skill.

## Lightweight execution envelopes

These are **planning scopes, not enforceable API token limits**. Actual usage may be `unknown` when the host does not expose it.

| Level | Resource policy |
|---|---|
| **QUICK** | One selected skill plus needed references, one requested output, no unrelated research or specialists |
| **GUIDED** (default) | Brief intake, only needed A-E dependencies; one owner question at a time; checkpoint after accepted work |
| **DEEP** (opt-in) | Wider research and full outputs only when requested; keep safeguards and business constraints |

1. **Route first, load later:** Read the shared orchestration and this guide once. Never preload all 18 business skills, agent briefs, checker source, tests or repository history. Load each selected `SKILL.md` and its required references immediately before use.
2. **Reuse evidence wisely:** Pass only frozen task inputs, relevant excerpts, approved business wording, source links and hashes. Do not repeatedly send the whole conversation or raw analytics. Reuse already authorized facts.
3. **Write proportionately:** A five-hook request returns five hooks. A CRO page audit prioritizes the first serious barrier. A full offer run still generates its required outputs and canonical SUMMARY, but not every unrequested skill document.
4. **Resume, don't restart:** Continue from CHECKPOINT and only reuse outputs whose frozen source hashes and decision versions still match. After a material change, invalidate and re-check affected downstream outputs and review receipts. Preserve the two-pass repair limit.
5. **Selective tools:** Search externally only when current facts materially affect the task and tools are available; do not invent results. Stop *unnecessary expansion*, not required QA, commercial decisions or independent-review obligations.
6. **Honest usage:** Distinguish requested from observed models and effort; report `unknown` rather than fabricated usage. **Do not drop evidence checks**, reviewer holds, declared business limitations, or required owner actions to save tokens.

This policy is instruction-level. Passing static checks does **not** prove automatic host routing, native specialist execution, independent reviewer provenance or measured token savings. Verify those separately using a fresh installed run.
