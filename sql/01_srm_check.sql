-- BigQuery Standard SQL. Run before viewing outcome metrics.
-- Assumes one assignment per eligible randomized customer; adapt table/filters.
-- For a prespecified 50/50 split, p < 0.001 (df=1) is the hard investigate gate.
-- chi-square >= 10.827566 is equivalent to p < 0.001; this flags SRM, not its cause.
WITH assigned AS (
  SELECT DISTINCT customer_id, variant
  FROM `project.dataset.experiment_events`
  WHERE experiment_id = 'auto_discount_vs_manual_coupon_v1'
    AND eligible = TRUE
), counts AS (
  SELECT variant, COUNT(DISTINCT customer_id) AS observed_n
  FROM assigned GROUP BY variant
), totals AS (
  SELECT COUNT(DISTINCT customer_id) AS total_n,
         COUNT(DISTINCT IF(variant = 'control', customer_id, NULL)) AS control_n,
         COUNT(DISTINCT IF(variant = 'treatment', customer_id, NULL)) AS treatment_n
  FROM assigned
), expected AS (
  SELECT 'control' AS variant, total_n * 0.5 AS expected_n FROM totals
  UNION ALL
  SELECT 'treatment', total_n * 0.5 FROM totals
), arms AS (
  SELECT e.variant, COALESCE(c.observed_n, 0) AS observed_n, e.expected_n
  FROM expected e LEFT JOIN counts c USING (variant)
), chi AS (
  SELECT SUM(SAFE_DIVIDE(POW(a.observed_n - a.expected_n, 2), a.expected_n)) AS chi_square,
         ANY_VALUE(t.total_n) AS total_n,
         ANY_VALUE(t.control_n) AS control_n,
         ANY_VALUE(t.treatment_n) AS treatment_n
  FROM arms a CROSS JOIN totals t
)
SELECT total_n, control_n, treatment_n,
       SAFE_DIVIDE(control_n, total_n) AS control_share,
       SAFE_DIVIDE(treatment_n, total_n) AS treatment_share,
       chi_square, ERFC(SQRT(chi_square / 2)) AS p_value_df1,
       chi_square >= 10.827566 AS srm_investigate_p_below_0_001
FROM chi;