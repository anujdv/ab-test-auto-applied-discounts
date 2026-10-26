# Pre-registration: automatic discount vs manual coupon

> **PLANNED TEMPLATE — NOT A COMPLETED REGISTRATION.** This document contains preliminary assumptions only. Replace bracketed items, verify economics with the business owner, and commit a dated, immutable version before observing experiment outcomes. No results are reported here.

## Contract metadata

- Status: Draft / pending approval
- Owner: [name]
- Registration timestamp (UTC): [YYYY-MM-DD HH:MM]
- Planned experiment window: [start date] to [end date]
- Experiment identifier: `auto_discount_vs_manual_coupon_v1`
- Data classification: synthetic data in this repository; real experiment data not supplied

## Business question and hypothesis

**If** eligible customers receive their eligible discount automatically rather than entering a coupon, **then** checkout conversion per randomized eligible customer will increase, **because** automatic application removes redemption friction.

The policy is only favorable if contribution margin per eligible customer remains within the pre-agreed non-inferiority bound and refund, payment failure, and support-contact guardrails do not materially worsen.

## Variants and eligibility

- **Control (50%)**: eligible customer sees the offer and must enter the same coupon manually.
- **Treatment (50%)**: same eligible offer is applied automatically; pricing, discount amount, copy, and checkout layout are otherwise held constant.
- Eligibility: [define geography, customer state, cart rules, channel, and exclusions before launch].
- Unit of randomization: stable customer ID; assignment persists across sessions and devices when identity is known.
- Exclude before assignment: [employees, test accounts, bots, ineligible carts, etc.]. Do not exclude post-randomization based on behavior.

## Outcomes and estimands

- **Primary**: binary checkout conversion within [e.g., 7 days] of first eligible assignment; denominator is every eligible randomized customer (ITT).
- **Key economic metric**: contribution margin per randomized eligible customer within the same window, including discount cost, refunds, and variable costs. Define source fields with Finance before launch.
- **Guardrails**: refund/cancellation rate, payment failure rate, average discount cost per eligible customer, and checkout support-contact rate. Define thresholds and windows before launch.
- **Exposure diagnostic**: share of assigned customers with a valid checkout exposure event. Exposure-based/ATT estimates are diagnostic only, not a replacement for ITT.

## Preliminary planning assumptions — validate before registration

These are placeholders for planning, not historical facts or observed results. The economic scenario below is illustrative and must be replaced with validated Finance inputs.

| Parameter | Preliminary assumption | Required action |
|---|---:|---|
| Control conversion | 18.5% | Replace with a trustworthy baseline for the exact eligible population |
| Minimum detectable absolute lift | +1.85 percentage points | Confirm it is both economically worthwhile and feasible |
| Allocation | 50/50 | Confirm operational capacity and any rollout constraints |
| Significance level | 5%, two-sided | Confirm with analytics policy |
| Power | 80% | Confirm before sample-size calculation |
| Outcome window | 7 days | Confirm attribution and refund maturation windows |
| Economic scenario | ₹2,500 AOV; 40% pre-discount gross margin; ₹150 discount; 60% manual redemption in Control and 100% in Treatment | Validate with Finance; illustration only |

Under that economic scenario, Control gross profit per converter is ₹1,000 − (0.60 × ₹150) = ₹910; Treatment gross profit per converter is ₹1,000 − ₹150 = ₹850. Break-even treatment conversion is 18.5% × ₹910 / ₹850 = 19.8059%, an absolute lift of about **+1.31 percentage points** (+7.1% relative). This is a conditional scenario calculation, not an observed business result. A +1.0 pp conversion lift would not break even on this simplified gross-profit model. The proposed +1.85 pp MDE is a rounded, more conservative planning target; it is not a claim that the effect will occur or that margin/other costs are immaterial.

With independent users, a two-sided two-proportion test, baseline 18.5%, MDE +1.85 pp, alpha 0.05, and power 80%, a normal-approximation calculation requires about **7,200 customers per arm (14,400 total)**. Use a validated sample-size implementation before registration. Increase the target only for prespecified clustering, delayed outcomes, or data loss. Do not stop early based on interim significance unless a sequential design is preregistered. For comparison, the prior 20% baseline / +1.0 pp plan needs roughly 26,400 per arm (52,800 total); a 55,000-customer seed default would align with that smaller MDE, not with the economically motivated +1.85 pp target.

## Decision rule (draft; approve before launch)

- First require a passing SRM check and valid instrumentation; otherwise hold the readout and investigate.
- Consider broad rollout only if the two-sided primary conversion test rejects at alpha 0.05 in the favorable direction, the confidence interval is compatible with the business MDE, and all economic/guardrail thresholds pass.
- Stage or hold if evidence is inconclusive, economics fail, or a guardrail crosses its agreed harm threshold. Define exact thresholds with Finance and Product before launch.
- One primary outcome and one planned analysis window. Segment analyses are exploratory and multiplicity-adjusted; no segment-only ship decision absent a new test.

## Change log

| Date | Change | Author / approver |
|---|---|---|
| [date] | Initial draft; assumptions remain unvalidated | [name] |
