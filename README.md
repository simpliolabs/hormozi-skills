# Hormozi Skills

![Hormozi Skills: build the offer, keep decisions under owner control](assets/readme/hormozi-hero.svg)

**Structured AI offer workflows with review gates and owner-controlled decisions.**

![License](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)
![Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Cursor-lightgrey)
![Inspired by](https://img.shields.io/badge/inspired%20by-Alex%20Hormozi-orange)

---

> An open-source, Hormozi-inspired skill library for Claude Code and Codex. Use standalone methods or a one-chat orchestrator to draft offers and sales materials. Controlled runs record business decisions, review obligations, and structural validation findings. Drafts do not constitute verified commercial claims or publication approval.

---

## The Problem

Building a compelling offer is hard. Most founders, coaches, and consultants either:

- Write vague offers that don't convert — *"I help people grow their business"*
- Price wrong — too low to be taken seriously, too high without justification
- Skip the sales layer entirely — no hooks, no pitch, no landing page copy

**hormozi-skills** provides a structured workflow: 17 business skills, a `hormozi-orchestrator` entry skill, five specialist role definitions, and output validation. The orchestrator requests specialist delegation when available; actual execution and any fallback must be reported, not assumed.

---

## What has actually been validated

![Evidence chart: original checker surfaced three of seven obligations; corrected replay preserved all seven](assets/readme/validation-evidence-chart.svg)


| Check | Evidence-backed result |
|---|---|
| PR #3 merged | [`b05b1c0`](https://github.com/simpliolabs/hormozi-skills/commit/b05b1c041b27b2fbf5bc4225ff14c48abaf40e2f) |
| Post-merge CI | [Windows and Ubuntu passed](https://github.com/simpliolabs/hormozi-skills/actions/runs/42110615431) |
| Bounded native acceptance | Seven **obligation identities** preserved in first completion, represented across six checker findings; no operator repair |
| Summary contract | Canonical offer summary, chosen hook, and three prioritized owner actions validated |
| Separate-context review | Missing/failed/stale/same-context receipts remain held; recorded receipts are **cooperative metadata**, not authenticated reviewer proof |
| Native specialist execution | **Not proven**; observed run used sequential fallback after a refused dispatch |

See the [acceptance report and evidence](docs/SEVEN_HOLD_VALIDATION.md). This is a bounded fictional-scenario result, **not** evidence of universal business accuracy, a real independent reviewer, or commercial readiness.

### How the system works

![Illustrated workflow: brief, orchestrator, draft assets, and checks with HELD or structural READY outcomes](assets/readme/workflow-illustrated.svg)

**Independent-review floor:** Controlled sales artifacts keep review holds even when an author marks `high_risk` false or leaves it out. Missing/failed/stale/same-context receipts do not satisfy separate-context review. See the [review policy](references/orchestration.md) and [validation evidence](docs/SEVEN_HOLD_VALIDATION.md).

A `READY` check is structural only. Pricing, guarantees, eligibility, claims, publication and external business actions remain under the owner's control.

---

## Quick Start

> **Install this fork:** The source below is `simpliolabs/hormozi-skills`. The original project by [Alex Smedile](https://github.com/alexsmedile/hormozi-skills) retains its attribution and MIT license.

### Claude Code

Add the marketplace, then install the plugin:

```bash
/plugin marketplace add simpliolabs/hormozi-skills
/plugin install hormozi-skills@hormozi-skills
```

Then invoke the `hormozi-orchestrator` agent or skill, or a specific business skill.

### Codex

Register the marketplace (a local clone of this repository, or its GitHub source), then install. The marketplace root is the repository root:

```bash
codex plugin marketplace add <path-to-clone-or-repo>
codex plugin list --available
codex plugin add hormozi-skills@hormozi-skills
```

Use the `hormozi-orchestrator` skill as the one-chat entry. If your Codex build does not discover it automatically, invoke it manually by naming the absolute path to its `SKILL.md` in your prompt. Non-interactive runs use `codex exec "<prompt>"`, and an interrupted run continues in the same session with `codex exec resume --last "<prompt>"` (both subcommands are listed by `codex exec --help`). Automatic activation and model/effort switching are not promised. The optional `.codex/` role adapters apply only when you work inside a trusted checkout of this repository; they are not copied into your project and do not register roles for a plugin installed elsewhere.

### Manual Install

If you want the raw skill files instead of the plugin flow:

```bash
# Clone the skill library
git clone https://github.com/simpliolabs/hormozi-skills.git
cd hormozi-skills

# Copy skills, agents AND the shared assets the skills load by plugin_root
cp -r skills/ agents/ references/ contracts/ scripts/ ~/.claude/
pip install -r requirements-qa.txt   # only for the optional output check
```

Skills and agents resolve `<plugin_root>/references/...` and `<plugin_root>/scripts/check_outputs.py` from their own base path, so `references/`, `contracts/` and `scripts/` must sit beside `skills/` and `agents/`. Output always goes to your project's `output/`, never into `~/.claude/`.

> [!TIP]
> Describe your business in plain language — rough idea, brain dump, or existing offer. The orchestrator interviews you, detects your stage, and builds everything from there.

---

## 📦 What You Get

The 11 business-content files below are generated as applicable. Controlled multi-step runs also produce `output/SUMMARY.md`, state, checkpoint, and QA records; not every focused request generates every artifact:

| File | What's Inside |
|------|--------------|
| `MARKET_RESEARCH.md` | Validated niche, pain map, demand signals |
| `OFFER.md` | Full Grand Slam Offer — avatar, obstacles, solution map, value stack |
| `OFFER_ANGLES.md` | 8 positioning angles, ranked |
| `OFFER_AUDIT.md` | Score per dimension + priority fixes |
| `VALUE_PERCEPTION.md` | Improved naming, packaging, framing |
| `BONUS_STACK.md` | Objection-killing bonus structure with perceived value |
| `PRICING.md` | Value-anchored price, tiers, justification story |
| `OBJECTIONS.md` | Hidden beliefs, belief shifts, DM-ready responses |
| `PITCH.md` | Short / medium / long pitch versions |
| `HOOKS.md` | 30+ hooks across 10 types, ranked |
| `LANDING_PAGE.md` | Full landing page copy, section by section |

---

## 🧠 Skills Library

Use any skill standalone — no orchestrator needed:

| Skill | Purpose |
|-------|---------|
| `hormozi-offer` | Build a Grand Slam Offer from scratch → `OFFER.md` |
| `hormozi-pitch` | Pitch deck and sales narrative |
| `hormozi-hooks` | Hook and headline generation (30+ hooks) |
| `audit-offer` | Score and rewrite an existing weak offer |
| `bonus-stack` | Build a bonus stack that kills objections |
| `business-model` | Choose and structure the right business model |
| `dfy-dwy-diy` | Frame offer as DFY / DWY / DIY tiers |
| `effort-reduction` | Reduce perceived effort in the offer |
| `idea-to-product` | Turn rough idea into productized offer |
| `landing-page-copy` | Generate landing page copy from an existing offer |
| `market-research` | Research market pain and demand signals |
| `objection-destroyer` | Map and neutralize common objections |
| `offer-angles` | Generate multiple positioning angles |
| `pricing-strategy` | Price anchoring and packaging |
| `productize` | Productize a service business |
| `value-accelerator` | Increase perceived value |
| `value-perception` | Improve how value is communicated |

> [!TIP]
> Skip the orchestrator and call any skill directly: `/audit-offer`, `/pricing-strategy`, `/landing-page-copy` — each works standalone with no prior context needed.

---

## 🔀 Agent System

```
hormozi-orchestrator
├── sub-market    → MARKET_RESEARCH.md
├── sub-offer     → OFFER.md + OFFER_ANGLES.md
├── sub-value     → OFFER_AUDIT.md + VALUE_PERCEPTION.md + BONUS_STACK.md
├── sub-pricing   → PRICING.md + OBJECTIONS.md
└── sub-sales     → PITCH.md + HOOKS.md + LANDING_PAGE.md
```

**Dependency order:** market → offer → (value ∥ pricing) → sales

The orchestrator selects tasks based on the owner's stage. It requests native specialist delegation where available, and must record refusal, fallback or unknown execution instead of claiming agents ran.

---

## ⚙️ How It Works

1. **Intake** — give the orchestrator anything: a raw idea, existing offer, brain dump, or sales page
2. **Interview** — focused questions one at a time, each with a suggested answer
3. **Stage detection** — classifies your situation (Stage A–E), shows which subagents will run
4. **Delegation** — requests specialists in dependency order where supported, recording any observed fallback or refusal
5. **Summary and checks** — produces `output/SUMMARY.md` with an offer paragraph, key decisions/holds, a chosen hook, and exactly three prioritized owner actions, then runs structural validation and reports HELD findings honestly

---

## Repo Structure

```
hormozi-skills/
├── skills/     # 17 business skills + hormozi-orchestrator entry (+ create-plugin)
├── agents/     # Orchestrator + 5 subagents
├── references/ # Shared workflow, evidence and feasibility contracts
├── contracts/  # JSON schemas for run records
├── scripts/    # check_outputs.py local acceptance checks
├── .codex/     # Optional Codex role adapters (trusted checkout only)
├── output/     # Generated offer documents (starts empty)
└── input/      # Drop existing offers, notes, or sales pages here
```

---

## Safe first use

Start with a **supervised, non-public** offer draft using verified inputs. Invoke `hormozi-orchestrator` in an installed checkout or use a focused skill. Review `output/SUMMARY.md`, `output/CHECKPOINT.md`, `output/QA_REPORT.md`, and the output checker's findings. Resolve or disclose unresolved business and independent-review obligations before any external use. The checker does not automatically verify market reality.

See [Operator guide](docs/OPERATING_GUIDE.md) for a first-run checklist, limitations and release boundaries.

---

## Who This Is For

- Founders, coaches, consultants, and freelancers building offers
- Anyone applying Hormozi's methodology who wants AI execution, not just AI advice
- Coding agents running offer-generation pipelines

## Who This Is Not For

- Generic copywriters looking for fill-in-the-blank templates — this thinks, it doesn't just fill
- Developers needing a code library — this is prompt-based, agent-native
- People who want a one-shot answer without iteration — the orchestrator interviews you

---

## Frameworks

Built on Alex Hormozi's offer methodology from *$100M Offers* and *$100M Leads*:

- Grand Slam Offer construction
- Value Equation: (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort and Sacrifice)
- Obstacle → solution reversal
- Value stack and bonus engineering
- Guarantee design (unconditional / conditional / effort-based)
- Price anchoring and perceived value
- Hook architecture (pattern interrupt, identity, outcome, curiosity)

---

## Credits

Originally created by [@alexsmedile](https://github.com/alexsmedile) and maintained in this fork at [simpliolabs/hormozi-skills](https://github.com/simpliolabs/hormozi-skills). Inspired by Alex Hormozi's publicly described frameworks; not affiliated with or endorsed by Alex Hormozi. Licensed under [MIT](LICENSE).
