---
name: market-research
description: Find the right market, extract real customer pain, and validate demand before building an offer. Use when you have an idea but no market, the niche feels too broad, or the offer is not converting. Generates micro-niches, scores them, extracts pain language, and creates a validation test plan — outputs MARKET_RESEARCH.md.
---

# Skill: Market Research & Demand (Starving Crowd Engine)

## Evidence & Authority Preflight

Applies to every task, including a single standalone request. No run files are needed.

- **Exact wording.** Quote customers and sources only from supplied or sourced material. Invented examples are labeled `synthetic` and never presented as real quotes, testimonials or results.
- **Unknown stays unknown.** A score, cost, volume or price nobody supplied is marked unknown, not zero and not a silent estimate.
- **Seller economics.** Check what the offer costs to deliver and what a refund or guarantee exposes. List missing cost inputs.
- **Simplest viable offer.** Add a component only for a named obstacle.
- **Proposal vs authorized.** Terms the owner has recorded are authorized; everything else is a proposal. Owner approval is not proof of a claim.
- **Qualified claims keep their conditions** every time they are repeated.
- **Requested quantity.** Return the number asked for (five hooks means five).
- **No deployment assertions.** Produce copy and handoff only. Never say anything is live, published, sent or scheduled.

Full rules: `<plugin_root>/references/evidence-contract.md`. Pricing math: `<plugin_root>/references/commercial-feasibility.md`. `<plugin_root>` is the plugin directory two levels above this skill's base path (the skill lives at `<plugin_root>/skills/<name>/`). Load packaged files by that absolute path, never relative to the working directory.

## Purpose
Find the right market, extract real pain, and validate demand before building an offer.

This skill prevents:
- building offers nobody buys
- targeting the wrong audience
- solving weak or low-urgency problems

Goal: identify a **starving crowd with real pain and buying intent**.

---

## When to Use
Activate this skill when:
- you have an idea but no market
- you are unsure who to target
- you want to validate demand before building
- your niche feels too broad
- your offer is not converting

---

## Inputs
This skill works with:
- a business idea
- a niche
- a skill or expertise
- a product concept
- or even a vague direction

---

## Core Outcome
The assistant produces:
- validated micro-niche
- clear target customer
- real pain statements
- demand signals
- buyer vs browser distinction
- validation strategy

---

# PART 1: Starving Crowd Finder

## Purpose
Find a group of people who:
- feel urgent pain
- actively look for solutions
- are willing to pay

---

## Assistant Behavior

### 1. Start from idea or skill
Extract:
- what problem is being solved
- who might have that problem

---

### 2. Generate micro-niches
Break broad markets into smaller groups:

Example:
- “fitness” → “busy dads over 35”
- “marketing” → “coaches under $5k/month”

---

### 3. Evaluate each niche

Check:

#### Pain Intensity
- how often they feel the problem
- how emotional it is

#### Purchasing Power
- can they afford solutions?

#### Accessibility
- can you reach them easily?

#### Growth
- is the market growing?

---

### 4. Score each niche

Score 1–10:

- pain
- money
- reachability
- growth

---

### 5. Select best niche
Choose:
- highest combined score
- strongest pain + ability to pay

---

## Output Format

```md
# MARKET_SELECTION.md

## 1. Idea
- Description

## 2. Micro-Niches
- Niche 1
- Niche 2
- Niche 3

## 3. Niche Scoring
- Pain:
- Money:
- Reach:
- Growth:

## 4. Selected Niche
- Final choice
- Reasoning
```

⸻

PART 2: Pain Extraction Skill

Purpose

Understand what the customer actually feels.

⸻

Assistant Behavior

1. Identify core problems

List:
	•	main frustrations
	•	repeated struggles
	•	emotional pain

⸻

2. Extract real language

Simulate or gather:
	•	how customers describe the problem
	•	informal phrasing
	•	emotional expressions

⸻

3. Create pain bullets

Types:

Surface Pain
	•	obvious problems

Deeper Pain
	•	emotional impact

Hidden Pain
	•	fears, doubts, frustrations

⸻

4. Generate “midnight thoughts”

What they think when:
	•	stressed
	•	frustrated
	•	alone

⸻

Output Format

```md
# CUSTOMER_PAIN.md

## 1. Core Problems
- Problem 1
- Problem 2

## 2. Raw Language
- Phrases customers use

## 3. Pain Bullets
- Surface pain
- Deeper pain
- Hidden pain

## 4. Emotional Triggers
- Fear
- Frustration
- Desire

## 5. Midnight Thoughts
- Thoughts they have at night
```

⸻

PART 3: Demand Validation Skill

Purpose

Confirm if the idea is worth building.

⸻

Assistant Behavior

1. Identify demand signals

Look for:
	•	people asking questions
	•	existing competitors
	•	paid solutions already in market
	•	repeated complaints

⸻

2. Classify audience

Split:

Buyers
	•	already spend money
	•	actively search for solutions

Browsers
	•	interested but not paying

⸻

3. Evaluate demand strength

Score:
	•	urgency
	•	willingness to pay
	•	competition level

⸻

4. Suggest validation tests

⸻

Pre-Sell Test
	•	offer before building
	•	gauge interest

⸻

Fake Door Test
	•	landing page + CTA
	•	measure clicks

⸻

Content Test
	•	post hooks
	•	track engagement

⸻

5. Create validation plan

Define:
	•	what to test
	•	how to test
	•	success criteria

⸻

Output Format

```md
# DEMAND_VALIDATION.md

## 1. Demand Signals
- Evidence found

## 2. Buyer vs Browser
- Buyers:
- Browsers:

## 3. Demand Score
- Urgency:
- Willingness to pay:
- Competition:

## 4. Validation Tests

### Test 1: Pre-Sell
- Plan:

### Test 2: Fake Door
- Plan:

### Test 3: Content
- Plan:

## 5. Validation Criteria
- What defines success
```

⸻

Combined Output

```md
# MARKET_RESEARCH.md

## 1. Selected Market
- Niche
- Reasoning

## 2. Customer Pain
- Pain bullets
- Emotional triggers
- Midnight thoughts

## 3. Demand Validation
- Signals
- Buyer vs browser
- Test plan
```

⸻

Decision Rules

Choose a niche when:
	•	pain is frequent
	•	emotion is strong
	•	money is available

Avoid markets when:
	•	pain is weak
	•	no urgency
	•	no proof of spending

Trust demand when:
	•	people pay already
	•	solutions exist
	•	complaints are frequent

⸻

Style Guidelines
	•	be specific
	•	use real language
	•	focus on pain
	•	avoid assumptions
	•	prioritize clarity

⸻

Success Criteria

The skill works when:
	•	a clear niche is selected
	•	pain is deeply understood
	•	demand is validated
	•	idea feels worth pursuing

## Skill-Specific Evidence Rules

- Label each pain quote, score and trend `supplied`, `sourced`, `inferred` or `synthetic`. Without interviews, browsing or transaction evidence, persuasive first-person language is synthetic messaging, not research.
- Never invent citations, quotes, demand validation or growth figures. Unknown growth stays unknown, and state your confidence.
- Niche scores need a stated basis; otherwise write `unknown`.
