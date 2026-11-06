# Commercial Feasibility (seller side)

Buyer value and price strategy stay in `pricing-strategy`. This reference adds the seller-economics pass that pricing must complete before a price is proposed as final.

## Two pricing modes

- **Packaging exploration** — tests options and bundles before scope is settled. Output is explicitly provisional.
- **Final feasibility** — runs against a *named offer version* after scope/guarantee are fixed. Required whenever scope, guarantee or delivery model changed after an earlier pricing pass.

## Inputs (each is a value, `unknown`, `not_requested` or `not_applicable`)

price and currency · billing cadence · deposit/payment plan · fulfillment cost per customer · payment fees · commissions/referrals · support load · capacity · CAC · refund/guarantee exposure.

Pricing never checks whether an audit or bonus file happens to exist. It receives the named input version or an explicit `not_requested`/`not_applicable`.

## Controlled priced-offer decision fields

For a controlled run that requests or writes `output/PRICING.md`, or runs a `sub-pricing/final_feasibility` task, root records these exact keys in `OFFER_DECISIONS.fields`. The read-only checker derives two separate unresolved commercial findings from the statuses even when a free-text blocker is generic or the run is already HELD. Matching is case-sensitive; `support_cost/capacity` is one field key.

| Obligation | Canonical key | Accepted existing aliases |
| --- | --- | --- |
| Refund terms | `refunds` | `refund_cancellation`, `refund_policy` |
| Cancellation terms | `cancellation` | `refund_cancellation`, `cancellation_terms`, `renewal/cancellation_terms` |
| Delivery cost | `delivery_cost` | `fulfillment_cost` (not `delivery`, which describes service scope) |
| Approved price | `price` | None; `price_anchor` is a proposal, not approval |
| Feasibility conclusion | `financial_feasibility` | None |
| Other declared cost inputs | Exact keys only | `acquisition_cost`, `CAC`, `cac`, `overhead`, `overhead_allocation`, `taxes`, `refund_cost`, `refund_costs`, `refund_cost_and_treatment`, `refund_exposure`, `guarantee_cost`, `affiliate_commission`, `payment_fees`, `support_cost/capacity` |

When canonical and alias keys coexist, every present source must be resolved; no preferred wording hides an unresolved value. A retained `superseded` alias remains a hold in the current decision record; preserve prior decision evidence when replacing it. Refund and cancellation terms need `status: approved`, nonempty policy text, and a nonempty `authorization_ref`; a numeric zero is not policy text. Delivery cost needs an approved structured money value, an authorization reference and at least one evidence reference. Price needs an approved money value and authorization reference. `financial_feasibility` needs an approved nonempty conclusion, authorization reference and evidence reference; every present cost key in the closed table needs an approved nonempty value and authorization reference. Missing fields, `unknown`, `proposed`, `held`, `superseded`, null values or missing references leave the relevant hold open. A real zero is a documented money value, never a substitute for unknown. These structural checks cannot authenticate owner approval or prove net profitability.

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
