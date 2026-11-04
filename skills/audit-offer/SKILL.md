---
name: audit-offer
description: Audit an offer to find weak points and get specific fixes. Use when an offer is not converting, conversions are low, or something feels off. Analyzes dream outcome, perceived likelihood, time delay, effort, market fit, value stack, pricing, messaging, and objections using the Hormozi Value Equation framework.
---

# Skill: Offer Audit (Weak Point Detector)

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
Analyze any offer and identify what is stopping it from converting.

This skill:
- finds weak points
- diagnoses why the offer underperforms
- suggests clear, practical fixes

Goal: turn a weak or average offer into a strong, obvious buy.

---

## When to Use
Activate this skill when:
- an offer is not selling
- conversions are low
- feedback is unclear or vague
- something feels “off” but you don’t know what
- you want to improve an existing offer

---

## Inputs
This skill works with:
- an `OFFER.md`
- a sales page
- a pitch
- a product or service description
- pricing and value stack
- audience description

---

## Core Outcome
The assistant produces:
- a full diagnosis of the offer
- a list of weak points
- severity level for each issue
- specific fixes
- prioritized action plan

---

## Audit Framework (Hormozi-Based)

The audit is based on:

- Dream Outcome
- Perceived Likelihood
- Time Delay
- Effort & Sacrifice

Plus:
- market clarity
- offer clarity
- delivery model
- value stack
- pricing
- messaging

---

## Assistant Behavior

### 1. Extract the offer
Identify:
- who it’s for
- what it promises
- how it works
- price
- format

Summarize:

> This offer helps X achieve Y using Z.

---

### 2. Evaluate Dream Outcome
Check:
- is the result clear?
- is it specific?
- is it desirable?
- is it urgent?

Weak signs:
- vague outcomes (“grow”, “improve”)
- no measurable result

---

### 3. Evaluate Perceived Likelihood
Check:
- is there proof?
- is the path clear?
- is it believable?

Weak signs:
- no testimonials
- unclear process
- big promises without support

---

### 4. Evaluate Time Delay
Check:
- how fast results happen
- when the first win occurs

Weak signs:
- long delay before results
- no quick wins

---

### 5. Evaluate Effort & Sacrifice
Check:
- how hard it feels
- how many steps are required
- how much discipline is needed

Weak signs:
- too many steps
- unclear instructions
- heavy effort

---

### 6. Evaluate Market Fit
Check:
- is the audience specific?
- is the pain urgent?
- can they pay?

Weak signs:
- “everyone” target
- low urgency problems

---

### 7. Evaluate Offer Structure
Check:
- is the offer easy to understand?
- is the structure clear?
- does it feel complete?

Weak signs:
- messy structure
- unclear components
- missing elements

---

### 8. Evaluate Value Stack
Check:
- is value clearly shown?
- are bonuses meaningful?
- is there a gap between value and price?

Weak signs:
- weak bonuses
- no stacking
- unclear value

---

### 9. Evaluate Pricing
Check:
- does price match value?
- is it justified?
- does it feel cheap or expensive?

Weak signs:
- random pricing
- no anchoring
- mismatch with outcome

---

### 10. Evaluate Messaging
Check:
- is it clear?
- is it specific?
- is it outcome-focused?

Weak signs:
- generic language
- unclear benefits
- no strong hooks

---

### 11. Evaluate Objections
Check:
- are objections handled?
- is risk reduced?
- is trust built?

Weak signs:
- no guarantee
- no objection handling
- unanswered doubts

---

## Output Format

```md
# OFFER_AUDIT.md

## 1. Offer Summary
- Who it’s for
- What it promises
- How it works
- Price

---

## 2. Overall Diagnosis
- Strengths
- Weaknesses

---

## 3. Value Equation Analysis

### Dream Outcome
- Score:
- Issues:
- Fixes:

### Perceived Likelihood
- Score:
- Issues:
- Fixes:

### Time Delay
- Score:
- Issues:
- Fixes:

### Effort & Sacrifice
- Score:
- Issues:
- Fixes:

---

## 4. Market Fit
- Issues:
- Fixes:

---

## 5. Offer Structure
- Issues:
- Fixes:

---

## 6. Value Stack
- Issues:
- Fixes:

---

## 7. Pricing
- Issues:
- Fixes:

---

## 8. Messaging
- Issues:
- Fixes:

---

## 9. Objections & Trust
- Issues:
- Fixes:

---

## 10. Top Priority Fixes
1. Fix
2. Fix
3. Fix

---

## 11. Quick Wins
- Fast improvements to implement immediately


⸻

Scoring System (Optional)

Each category scored 1–10:
	•	1–3 = critical issue
	•	4–6 = needs improvement
	•	7–8 = solid
	•	9–10 = strong

⸻

Decision Rules

Fix outcome first when:
	•	it’s unclear
	•	it’s not compelling

Add proof when:
	•	trust is low
	•	claims feel weak

Reduce effort when:
	•	execution feels heavy
	•	drop-off is high

Reduce time when:
	•	results feel far away
	•	motivation is low

Improve messaging when:
	•	people don’t understand quickly
	•	hooks feel weak

⸻

Before vs After Example

Before
	•	unclear offer
	•	weak value
	•	low conversions

After
	•	clear outcome
	•	strong value stack
	•	better positioning
	•	higher conversions

⸻

Style Guidelines
	•	direct and honest
	•	no fluff
	•	clear problems and fixes
	•	actionable insights

⸻

Success Criteria

The skill works when:
	•	weak points are obvious
	•	fixes are clear and actionable
	•	the offer becomes stronger
	•	conversions improve

## Skill-Specific Evidence Rules

- Score only what the evidence supports. A dimension without evidence is `unknown`, not a low or middling number.
- A diagnostic audit diagnoses and does not rewrite. A later revised check is a separate document that never overwrites the original.
- An audit proposes fixes. It does not approve claims or terms.
