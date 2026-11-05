# Adaptive routing: approachable for beginners, economical for experts

This is normative routing guidance for the *existing* `hormozi-orchestrator` root. It does not introduce a new agent, schema, task mode, workflow phase, permission, or automatic model switch. Use alongside `<plugin_root>/references/orchestration.md`, `<plugin_root>/references/cro-waterfall.md`, and the original standalone skill methods.

## The two front doors

**Beginner / unsure of the next step:** A natural request such as "I have an idea", "help me build a business offer", "my offer isn't working", or "I don't know where to start" should select the main orchestrator *if the installed host discovers it*. Reflect known context briefly; ask **one high-value question at a time**, suggesting a plausible answer. Do not expose A-E stages, specialist role names, directory paths or task ledgers until relevant. If the user cannot answer, propose a provisional assumption labelled `inferred` and request its validation, rather than interrogating endlessly.

**Expert / precise request:** "Write five hooks", "audit pricing", "review this landing page", or "draft a pitch" should invoke the corresponding standalone skill, complete the requested quantity, and stop. The full waterfall is not a prerequisite to using a focused method. If missing business facts block a safe output, identify the precise gap; do not silently expand into market + offer + value + pricing.

**Important:** Natural-language auto-activation is host-dependent. Advertise real explicit selection as the dependable fallback. No special `/offer` command exists in this repo until a separately tested alias is added.

## Scope routing: smallest sufficient graph

| User need | Selected route | Default CRO work |
|---|---|---|
| New idea / complete offer | Interview briefly, Stage A as needed: market -> offer -> value -> final pricing -> owner reconciliation -> requested sales | Root CRO readiness gate before final SUMMARY/checker |
| Existing offer not converting | Stage B original diagnostic -> authorized revision -> revised check -> final feasibility -> requested sales | Root CRO full page only if page evidence exists, otherwise readiness/handoff |
| Business scale / packaging | Stage D with only affected offer/pricing branches | Root CRO readiness or offline buyer-handoff |
| Specific sales asset on authorized offer | Stage C sales-only, no unauthorized repricing | Root CRO gate only if digital conversion destination is in scope |
| One specific skill task | Focused single method, no controlled full-run ledger | No automatic full CRO gate; use standalone evidence preflight |
| Direct CRO/SEO/form audit | `cro-page-optimizer` directly, not forced market/offer rebuild | Full available-evidence audit |
| Multi-step custom / unclear | Stage E smallest dependencies justified by owner goal | CRO gate if an offer workflow, not for unrelated work |

**All standalone skills still apply the shared evidence and commercial authority preflight.** They do **not** all trigger the complete waterfall. "Automatic CRO" means eligible full offer workflows include a root-owned gate, not that every user message triggers every skill or specialist.

## Lightweight execution budgets

The objective is **minimum sufficient evidence, methods and output**, not a fixed universal token number. These are planning envelopes, **not enforceable API token limits**. If the host provides usage data, report actual use; otherwise say `unknown`.

| Level | When | Default scope |
|---|---|---|
| **QUICK** | Specific deliverable, e.g., five hooks | Load one selected method and its required references; brief answer or requested artifact only; no background market research, no extra specialists, no run records |
| **GUIDED** (default) | Owner needs direction or a multi-step offer | Interview one unknown at a time; plan a narrow A-E route; execute the next needed stage rather than all 18 business skills; commit a checkpoint, then resume only affected stages |
| **DEEP** (opt-in) | Explicit research, competitive analysis, multi-page implementation or exhaustive review | Propose additional data/tool scope and deliverables before expensive expansion; preserve legitimate review gates and needed evidence. The user decides whether to widen scope |

Efficiency controls:

1. **Decide the route first.** Read `<plugin_root>/references/orchestration.md` once. Do not preload every standalone skill, specialist role, reference, test file, or repository archive. Load the selected skill's **actual** `SKILL.md` and only its required references immediately before executing that task.
2. **One owner interview.** Ask a single question only when material input is missing; reuse already supplied or authorized facts. Do not ask the specialist to interview the owner again.
3. **Small, frozen briefs.** Pass only the selected task's frozen source excerpts and required hashes. Avoid re-sending the entire chat history, duplicate screenshots, or unrelated analytics. Summarize evidence with source links, date and constraints, but retain verbatim approved commercial terms where needed.
4. **No automatic overproduction.** A hooks request gets its requested hooks. A focused CRO audit gets the first barrier and prioritized fixes. A full offer run produces its defined requested artifacts and canonical SUMMARY, but should not independently produce 18 skill deliverables unless they are required.
5. **Checkpoint/reuse safely.** Reuse accepted artifacts only when their input hashes and decision versions match. Resume from the recorded checkpoint; a changed price/claim invalidates affected downstream outputs and review receipts.
6. **Research selectively.** Search the web or connected sources only when the owner's requested job needs facts and the environment permits it. Never invent sources, research, outcomes, testimonials or platform measurements to avoid a tool call.
7. **Stop expansion, not safeguards.** When a decision or independent review is unresolved, keep all documented blockers in RUN_STATE, CHECKPOINT and QA_REPORT, deliver the useful provisional draft, and request the owner decision. Do not drop evidence checks, required reviews, safety or the canonical SUMMARY to meet a budget.
8. **Report effort honestly.** Distinguish requested model/effort from observed values; record `unknown` when runtime usage is invisible. A prompt-level "budget" is not a guaranteed cap on token billing or compute.

## Simple "start here" conversation

User: "I have a business idea, but no idea what to ask."

Orchestrator: "I can help you turn it into an offer. What would you like to sell, even roughly? For example: a service, a product, or a membership."

After the reply, classify the relevant A-E route and show a one-sentence plan. Ask only for the next essential fact, not a 20-question form. For a large multi-step run, perform the default CRO readiness gate *when downstream sales work is available*, not as an expensive preliminary full site audit.

Expert: "Give me five tested-looking Instagram hooks for this approved offer."

Router: load `hormozi-hooks` only. Do not label hooks "tested" without real experiment data. Return five provisional hooks and disclose necessary claim limits. No forced CRO task ledger.

## What has not been proven

This reference is **instruction-level routing**. Static tests and successful unit tests do not prove a particular host auto-selected the orchestrator, delegated distinct specialist agents, respected a quantitative token cap, or performed an independent separate-context review. Those require fresh controlled native acceptance and actual runtime evidence.
