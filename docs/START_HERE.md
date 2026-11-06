# Start here: your goal is enough

You do **not** need to know skill names, agents, schemas, or the A-E stage labels. Install the [Simpliolabs fork](../README.md#quick-start), then describe what you're trying to accomplish. The skills should route by goal and load only the needed methods. Host-specific auto-selection is not guaranteed, so use the explicit selector listed below when necessary.

## Choose a starting point

| Your situation | Copy this first message | What runs |
|---|---|---|
| **I am not sure what I need** | "I have a business idea. Help me figure out what to do first; ask me one question at a time." | Guided orchestrator, minimal initial intake; the offer workflow only after your goal is clear |
| **I want the whole offer** | "Build a complete offer and sales funnel for [my business]. Use my real facts; mark unknowns and approvals." | Relevant market/offer/value/pricing/sales dependencies, automatic downstream CRO, required QA/holds |
| **I have an offer that is underperforming** | "My current offer isn't converting. Review the attached offer and find the first real blocker." | Stage-B diagnostic, smallest revision path, CRO for the conversion surface if available |
| **I know the exact task** | "Write exactly five hooks for this approved offer." | Hooks method only; no full orchestrator run |
| **I have a checkout or landing-page problem** | "Use my screenshot and Clarity summary to diagnose why visitors abandon this page." | CRO Page Optimizer directly, without an automatic offer rebuild |

## How the two entry styles behave

**Guided:** Ask one material question, with a reasonable example. Explain the route in ordinary language. If key facts are missing, keep them unknown. Run only the next necessary work. A full workflow includes the downstream CRO gate by default; it does not use every skill.

**Focused:** Directly use the relevant standalone skill and its required references. Return only the requested output. Still apply common evidence rules and owner-controlled terms, but do not create an A-E pipeline, read all skill files or run unrelated specialists.

**Deep-dive (you request it):** Say "Do the complete research and implementation audit" or supply an expanded scope. The assistant should confirm which extra research and output are relevant before expanding. This is not a guaranteed compute or billing limit.

## Cost and context discipline

- Do not load 18 business methods upfront. Load a method **only when its task is selected**.
- Do not duplicate entire transcripts or unneeded analytics in every specialist task; pass short frozen briefs and source/decision references.
- Do not redo accepted work when its hashes and owner-approved terms are unchanged. Resume from the last valid checkpoint.
- Avoid generating market, full offer, pricing, CRO and sales files for one simple "five hooks" request.
- Do not claim measured token savings unless the host provides actual token usage. Prompt guidelines alone cannot hard-cap compute.
- Never skip evidence checks, legal/business holds, or needed independent review just to save resources.

## Activate the right skill

In a compatible host, natural language may select the intended skill automatically. If it doesn't:

- **Claude Code:** Use the slash command/skill picker and explicitly choose the installed `hormozi-orchestrator` or `cro-page-optimizer`.
- **Codex:** Explicitly select the installed skill, e.g. `$hormozi-orchestrator` or `$cro-page-optimizer` if supported in the installed version.
- **ChatGPT:** If installed and available, use the skill selector via `@` to choose it.

A short `/offer` alias is only a **proposal** until separately implemented and tested in the target host.

## What does "READY" mean?

The current checker tests structure and known obligations. A `READY` result does **not** mean an independent reviewer actually ran, claims are independently verified, or a business asset is approved for publication. A `HELD` result can contain useful drafts while required reviews, owner approvals and evidence remain unresolved.

For the precise route matrix, see [Adaptive routing](../references/adaptive-routing.md). For the default downstream CRO rule, see [CRO waterfall](../references/cro-waterfall.md). For the recorded, bounded acceptance evidence, see [tested behavior and limits](../README.md#tested-behavior-and-known-limits).
