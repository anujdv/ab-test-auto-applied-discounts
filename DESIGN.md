# Experiment design and analysis plan

> **Planned design template.** No experiment has run. Validate assumptions, schema, and thresholds before launch; this is not a claim of causal findings.

## Design

Randomize eligible customers 1:1 using a stable customer identifier. Control requires manual entry of the eligible coupon; treatment applies the same discount automatically. Keep all other checkout experiences constant. Assignment should be persistent across sessions and devices when customer identity is available.

The primary estimand is the **intent-to-treat (ITT)** difference in conversion among all eligible randomized customers, regardless of whether a checkout exposure event was logged. This preserves the benefit of randomization and captures implementation failures as part of the policy effect. An exposure/actually-treated estimate is secondary and potentially biased by post-assignment behavior.

## Assumptions and threats

- **SUTVA / no interference**: one customer's assignment does not affect another customer's outcome; promotions should not cause stockouts or shared household contamination.
- **Consistency**: each arm delivers the specified offer, amount, and checkout experience throughout the test.
- **Stable identity**: avoid duplicate customer IDs and cross-arm exposure; document anonymous-to-known identity merges.
- **Concurrent changes**: freeze or log pricing, campaign, checkout, and inventory changes; avoid overlapping experiments on the same funnel.
- **Logging**: assignment, eligibility, exposure, order, discount, refund, and guardrail events need stable IDs and timestamps.
- **Missing outcomes**: define attribution window and late-arriving orders before analysis; do not assume missing means no conversion without validation.

## Checks before outcomes

1. Run `sql/01_srm_check.sql` on assigned eligible customers. A statistically significant mismatch or material allocation deviation requires investigation before outcome analysis.
2. Validate duplicate assignments, eligibility, treatment delivery, timestamps, and outcome joins.
3. Run `sql/02_exposure.sql` to quantify exposure and cross-arm issues. ITT remains primary.

## Statistical analysis

- Primary outcome: conversion proportion per assigned customer; report arm counts/rates, absolute difference (treatment minus control), relative lift, two-sided two-proportion z-test, and 95% confidence intervals.
- Key economics: contribution margin per assigned customer, with a prespecified estimator and interval appropriate to the distribution. The proportion helper in `analysis/stats.py` does not analyze revenue.
- Guardrails: report arm rates and intervals; compare against thresholds frozen in the pre-registration.
- Alpha: preliminary two-sided 0.05 for one primary metric. Do not repeatedly inspect significance without a sequential plan.
- Segments: exploratory; `sql/04_segmentation.sql` uses Bonferroni adjustment across the returned segment rows. Define this family before interpreting results.
- Missingness, extreme values, and metric definitions must be handled according to the frozen plan, not selected after observing lift.

## SQL data contract (illustrative)

The SQL templates use BigQuery Standard SQL and assume `project.dataset.experiment_events` has one row per customer with:

`experiment_id INT64` (301), `variant_id INT64` (3011/3012), `customer_id STRING`, `variant STRING` (`control`/`treatment`), `eligible BOOL`, `assigned_at TIMESTAMP`, `exposed BOOL`, `exposure_count INT64`, `converted BOOL`, `order_count INT64`, `revenue NUMERIC`, `discount_cost NUMERIC`, `contribution_margin NUMERIC`, `refund BOOL`, `payment_failed BOOL`, `support_contact BOOL`, `device STRING`, `country STRING`, `category STRING`.

Adapt table and field names and verify grain before running. If source data is event-level, first build a deduplicated customer-level analysis table with a documented attribution rule.

