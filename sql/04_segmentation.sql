-- BigQuery Standard SQL. Exploratory slices; Bonferroni family = returned rows.
-- Review sparse cells and define segment family before interpretation.
WITH user_segments AS (
  SELECT customer_id, variant, converted, device, country, category
  FROM `project.dataset.experiment_events`
  WHERE experiment_id = 301
    AND eligible = TRUE
), long_segments AS (
  SELECT customer_id, variant, converted, 'device' AS segment_type, device AS segment_value FROM user_segments
  UNION ALL SELECT customer_id, variant, converted, 'country', country FROM user_segments
  UNION ALL SELECT customer_id, variant, converted, 'category', category FROM user_segments
), agg AS (
  SELECT segment_type, segment_value,
         COUNTIF(variant = 'control') AS n_control,
         COUNTIF(variant = 'control' AND converted) AS x_control,
         COUNTIF(variant = 'treatment') AS n_treatment,
         COUNTIF(variant = 'treatment' AND converted) AS x_treatment
  FROM long_segments GROUP BY segment_type, segment_value
), calc AS (
  SELECT *, SAFE_DIVIDE(x_control,n_control) AS p_control,
         SAFE_DIVIDE(x_treatment,n_treatment) AS p_treatment,
         SAFE_DIVIDE(x_treatment,n_treatment)-SAFE_DIVIDE(x_control,n_control) AS risk_difference,
         SAFE_DIVIDE(x_control+x_treatment,n_control+n_treatment) AS pooled_p
  FROM agg
), test AS (
  SELECT *, SAFE_DIVIDE(risk_difference,
      SQRT(pooled_p*(1-pooled_p)*(SAFE_DIVIDE(1.0,n_control)+SAFE_DIVIDE(1.0,n_treatment)))) AS z_stat
  FROM calc WHERE n_control > 0 AND n_treatment > 0
), pvals AS (
  SELECT *, ERFC(ABS(z_stat)/SQRT(2)) AS p_value_two_sided,
         COUNT(*) OVER() AS bonferroni_family_size
  FROM test
)
SELECT *, LEAST(1.0, p_value_two_sided * bonferroni_family_size) AS bonferroni_adjusted_p,
       LEAST(1.0, p_value_two_sided * bonferroni_family_size) < 0.05 AS adjusted_p_below_0_05
FROM pvals ORDER BY segment_type, segment_value;

