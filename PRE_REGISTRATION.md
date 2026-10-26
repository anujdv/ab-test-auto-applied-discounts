# Pre-registration: automatic discount vs manual coupon

> **SIMULATION PLAN — NOT A REAL EXPERIMENT REGISTRATION.** This dated plan is for generating and practicing analysis on synthetic data only. No customer database is connected, no real experiment has run, and no results are reported. The business assumptions below are illustrative and are not approved Finance inputs.

## Contract metadata

- Status: Simulation plan drafted; real experiment pending business and analytics approval
- Owner: Anuj (repository owner; confirm before any real experiment)
- Simulation plan timestamp (UTC): 2026-10-26 08:58
- Planned simulation: Generate one synthetic customer-level dataset on 2026-10-26; this is not a live test window or a 14-day experiment
- Experiment identifier: `auto_discount_vs_manual_coupon_v1`
- Data classification: synthetic data only; real experiment data not supplied

## Business question and hypothesis

**If** eligible customers receive their eligible discount automatically rather than entering a coupon, **then** checkout conversion per randomized eligible customer will increase, **because** automatic application removes redemption friction.

For a real business decision, the policy is only favorable if contribution margin per randomized eligible customer meets a Finance-approved non-inferiority bound and refund, payment failure, and support-contact guardrails stay within approved limits. Those thresholds have not been provided, so this simulation cannot support a rollout decision.

## Variants and eligibility

- **Control (50%)**: synthetic eligible customer sees the offer and must enter the same coupon manually.
- **Treatment (50%)**: same synthetic offer is applied automatically; simulated pricing, discount amount, copy, and checkout layout are otherwise held constant.
- Simulation eligibility: every generated synthetic customer is eligible. This does not define eligibility for a real customer population.
- Unit of randomization: stable synthetic customer ID. Assignment is generated deterministically and remains the same for that customer ID.
- Real-experiment eligibility and exclusions (geography, customer state, cart rules, channel, employees, test accounts, bots, and ineligible carts) remain **to be defined before a real launch**. Do not exclude real participants after assignment based on behavior.

## Outcomes and estimands

- **Primary**: binary checkout conversion in the synthetic outcome record; use a 7-day outcome window as a planning example only. The generator creates a binary outcome and does not model the timing of a purchase within those seven days. For any real test, confirm the window and use every eligible randomized customer in the denominator (ITT).
- **Key economic metric**: contribution margin per assigned synthetic customer, used only to demonstrate the calculation. For a real test, Finance must define source fields and how discounts, refunds, and variable costs are counted.
- **Guardrails**: refund/cancellation, payment failure, discount cost per assigned customer, and checkout support-contact rates are generated as illustrative fields. Real thresholds and measurement windows remain to be agreed with Finance and Product.
- **Exposure diagnostic**: share of assigned synthetic customers with a generated exposure flag. Exposure-based/ATT estimates are diagnostic only, not a replacement for ITT.

## Preliminary planning assumptions — validate before real registration

These are placeholders for planning, not historical facts or observed results. The economic scenario is illustrative and must be replaced with validated Finance inputs before any real experiment.

| Parameter | Simulation assumption | Required action before real test |
|---|---:|---|
| Control conversion probability | 18.5% | Replace with a trustworthy baseline for the exact eligible population |
| Treatment conversion probability | 20.35% | Synthetic illustration of a +1.85 pp difference; not an expected or observed result |
| Minimum detectable absolute lift (MDE) | +1.85 percentage points | Confirm it is economically worthwhile and feasible |
| Allocation | 50/50 | Confirm operational capacity and any rollout constraints |
| Significance level | 5%, two-sided | Confirm with analytics policy |
| Power | 80% | Recalculate with validated inputs and an approved method |
| Outcome window | 7 days | Confirm attribution and refund maturation windows |
| Economic scenario | ₹2,500 average order value; 40% pre-discount gross margin; ₹150 discount; 60% manual redemption in Control and 100% in Treatment | Illustrative only; validate with Finance |

Under that illustrative economic scenario, the assumed pre-discount gross margin per ₹2,500 order is ₹1,000 (₹2,500 × 40%). Control's average discount cost per converter is ₹90 (60% × ₹150), leaving ₹910. Treatment's discount is always applied, leaving ₹850. Break-even Treatment conversion is 18.5% × ₹910 / ₹850 = 19.8059%, or about **+1.31 percentage points** above Control (+7.1% relative). This is a conditional example, not an observed business result. A +1.0 pp lift would not break even under this simplified gross-profit calculation. The proposed +1.85 pp MDE is a rounded planning target above that estimated break-even point; it does not guarantee profitability or account for unmodeled costs.

With independent users, a two-sided two-proportion test, baseline 18.5%, MDE +1.85 pp, alpha 0.05, and power 80%, a normal-approximation calculation requires about **7,200 customers per arm (14,400 total)**. The generator's 15,000 default is a convenient synthetic practice size near that target; actual generated group sizes may differ slightly from 50/50. Recalculate for a real test and increase the target only for prespecified clustering, delayed outcomes, or data loss. Do not stop early based on interim significance unless a sequential design is preregistered. For comparison, the previous 20% baseline / +1.0 pp plan needs roughly 26,400 per arm (52,800 total); a 55,000-customer seed default would align with that smaller MDE, not with this +1.85 pp target.

## Decision rule (simulation demonstration only; real thresholds pending)

- Demonstrate the SRM check and validate synthetic instrumentation before viewing simulated outcome comparisons.
- The simulated conversion comparison is a code/workflow demonstration only. Do not use it to recommend shipping, estimate actual business impact, or make claims about real customers.
- For a real experiment, require a passing SRM check and valid instrumentation, then consider rollout only if the primary result favors Treatment and Finance-approved economic and guardrail thresholds pass.
- Hold a real readout if evidence is inconclusive, economics fail, or an agreed guardrail crosses its harm threshold. Define exact thresholds with Finance and Product before launch.
- One primary outcome and one planned analysis window. Segment analyses are exploratory and multiplicity-adjusted; no segment-only ship decision absent a new test.
- The brief's 14-full-day minimum applies to a real test for weekly cycles; this synthetic one-shot dataset has no calendar runtime and cannot assess seasonality or novelty effects.

## Change log

| Date | Change | Author / approver |
|---|---|---|
| 2026-10-26 | Clarified assumptions and scope for a synthetic practice run; real eligibility, dates, economics, and thresholds remain unapproved | Codex-assisted draft; owner review pending |
