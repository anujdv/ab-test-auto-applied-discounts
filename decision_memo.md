# Synthetic case-study readout — automatic discount vs manual coupon

> **SYNTHETIC PRACTICE RESULTS ONLY.** This was not a real customer experiment. Do not use this memo to recommend a real rollout or claim an effect on actual shoppers.

## Executive summary

The notebook demonstrates a customer-level A/B analysis workflow using 15,000 generated records (seed `20261021`). The generator deliberately assigns a higher conversion probability to Treatment (20.35%) than Control (18.5%). The observed Treatment lift is therefore a programmed feature of the simulation, not evidence of causality.

**No real Ship / Stage / Hold decision is made.** Real guardrail thresholds and Finance-approved economics were not provided.

## Simulated scorecard

| Measure | Control | Treatment | Treatment − Control | Practice interpretation |
|---|---:|---:|---:|---|
| Assigned customers | 7,561 | 7,439 | — | 15,000 total; each arm exceeds the approximate 7,200 target |
| SRM check | 7,561 observed vs 7,500 expected | 7,439 observed vs 7,500 expected | χ²(1)=0.992, p=0.319 | No flag at the preregistered p < 0.001 investigate threshold |
| ITT conversion | 1,432 / 7,561 (18.94%) | 1,522 / 7,439 (20.46%) | +1.52 pp; 95% CI +0.25 to +2.79 pp; p=0.0192 | Synthetic output; lift is encoded in generator |
| Contribution margin / assigned customer | ₹168.15 | ₹169.22 | +₹1.08; approx. 95% interval −₹10.03 to +₹12.19 | Interval includes zero; illustrative model only |
| Refund rate | 36 / 7,561 (0.48%) | 41 / 7,439 (0.55%) | — | Descriptive; no threshold specified |
| Payment-failure rate | 146 / 7,561 (1.93%) | 152 / 7,439 (2.04%) | — | Descriptive; no threshold specified |
| Support-contact rate | 316 / 7,561 (4.18%) | 308 / 7,439 (4.14%) | — | Descriptive; no threshold specified |

## What the checks mean

The generated assignment split is close to the planned 50/50 allocation. The SRM chi-square p-value is above 0.001, so this dataset does not trigger the predefined investigate rule. This checks the simulated counts; it does not validate a live assignment or logging system.

The conversion comparison is intent-to-treat: every assigned eligible synthetic customer is included, regardless of the exposure flag. The observed +1.52 pp estimate is below the planned +1.85 pp MDE, while its confidence interval spans values below and above +1.85 pp. The MDE is a planning input for sample size, not a guaranteed minimum effect or a pass/fail threshold.

## Economic assumptions and uncertainty

The generator assumes average order value ₹2,500, gross margin before discount 40% (₹1,000 per order), a ₹150 discount, coupon use by 60% of Control converters, and automatic discounting for all Treatment converters. It sets contribution margin to zero for a refunded order and subtracts no other operating costs. These inputs are illustrative and are not Finance-approved.

The reported large-sample interval for the mean margin difference uses the observed per-customer contribution-margin variance in each arm. It is approximately −₹10.03 to +₹12.19, so this simulated run does not establish a positive contribution-margin effect. The simple break-even scenario in the pre-registration also omits unmodeled costs and is not a profit forecast.

## Limitations

- All customer IDs, assignment, outcomes, exposure flags, and financial values are synthetic.
- Conversion probabilities are intentionally set to 18.5% for Control and 20.35% for Treatment.
- Exposure is generated independently of conversion; the nominal seven-day window is not simulated over time.
- Device, country, and category labels are illustrative, not representative.
- No real guardrail thresholds or Finance-approved economic estimator were supplied.
- No rollout recommendation or real business impact estimate follows from this dataset.

## What a real decision would require

Before a live experiment, the business would need to approve eligibility and identity rules, validated event and financial definitions, an outcome window, sample size based on verified inputs, guardrail thresholds, an exposure/instrumentation plan, and a preregistered decision rule. The live assignment and outcomes would then need validation before interpretation.
