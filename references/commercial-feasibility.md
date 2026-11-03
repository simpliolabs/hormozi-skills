# Commercial Feasibility (seller side)

Buyer value and price strategy stay in `pricing-strategy`. This reference adds the seller-economics pass that pricing must complete before a price is proposed as final.

## Two pricing modes

- **Packaging exploration** — tests options and bundles before scope is settled. Output is explicitly provisional.
- **Final feasibility** — runs against a *named offer version* after scope/guarantee are fixed. Required whenever scope, guarantee or delivery model changed after an earlier pricing pass.

## Inputs (each is a value, `unknown`, `not_requested` or `not_applicable`)

price and currency · billing cadence · deposit/payment plan · fulfillment cost per customer · payment fees · commissions/referrals · support load · capacity · CAC · refund/guarantee exposure.

Pricing never checks whether an audit or bonus file happens to exist. It receives the named input version or an explicit `not_requested`/`not_applicable`.

## Arithmetic

Money is integer minor units + currency + cadence. Do not mix cadences (an annual refund policy is not a monthly one).

- Contribution before omitted costs = price − known variable costs.
- Margin before omitted costs = contribution ÷ price.
- Example: price 2,500, fulfillment 2,200 → contribution 300, **12 %** *before* omitted costs. Label it "before CAC, fees, commissions and support", **not** verified net profit.
- Missing inputs are listed, not assumed zero. Scenarios (best / expected / worst) are labelled as scenarios.

## Guarantee exposure

State refund conditions, eligibility and time window exactly. A guarantee that is "not live" (policy not operational) is excluded from copy. Compute exposure only from stated refund-rate assumptions and label them as assumptions.

## Output

Return: recommended price proposal, inputs used (with unknowns), contribution/margin with caveats, guarantee exposure, and what would change the recommendation. If pricing changes scope or guarantee, hand only the affected work back to root for revision; after two unsuccessful repair passes, surface the disagreement.
