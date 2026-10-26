-- BigQuery Standard SQL. Run before viewing outcome metrics.
-- Assumes one row per eligible randomized customer; adapt table/filters.
-- For a prespecified 50/50 split, p < 0.001 (df=1) is the hard investigate gate.
-- chi-square >= 10.827566 is equivalent to p < 0.001; this flags SRM, not its cause.
WITH assigned AS (
  SELECT customer_id, variant
  FROM `project.dataset.experiment_events`
  WHERE experiment_id = 'auto_discount_vs_manual_coupon_v1'
    AND eligible = TRUE
), counts AS (
  SELECT variant, COUNT(DISTINCT customer_id) AS observed_n
  FROM assigned GROUP BY variant
), totals AS (
  SELECT SUM(observed_n) AS total_n,
         SUM(IF(variant = 'control', observed_n, 0)) AS control_n,
         SUM(IF(variant = 'treatment', observed_n, 0)) AS treatment_n
  FROM counts
), expected AS (
  SELECT 'control' AS variant, total_n * 0.5 AS expected_n FROM totals
  UNION ALL
  SELECT 'treatment', total_n * 0.5 FROM totals
), chi AS (
  SELECT SUM(POW(c.observed_n - e.expected_n, 2) / e.expected_n) AS chi_square,
         ANY_VALUE(t.total_n) AS total_n,
         ANY_VALUE(t.control_n) AS control_n,
         ANY_VALUE(t.treatment_n) AS treatment_n
  FROM counts c JOIN expected e USING (variant) CROSS JOIN totals t
)
SELECT total_n, control_n, treatment_n,
       SAFE_DIVIDE(control_n, total_n) AS control_share,
       SAFE_DIVIDE(treatment_n, total_n) AS treatment_share,
       chi_square, ERFC(SQRT(chi_square / 2)) AS p_value_df1,
       chi_square >= 10.827566 AS srm_investigate_p_below_0_001
FROM chi;
