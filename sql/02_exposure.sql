-- BigQuery Standard SQL. Assignment-level exposure diagnostic; ITT remains primary.
WITH assigned AS (
  SELECT customer_id, variant, exposed, exposure_count, converted
  FROM `project.dataset.experiment_events`
  WHERE experiment_id = 301
    AND eligible = TRUE
)
SELECT variant,
       COUNT(DISTINCT customer_id) AS assigned_customers,
       COUNT(DISTINCT IF(exposed, customer_id, NULL)) AS exposed_customers,
       SAFE_DIVIDE(COUNT(DISTINCT IF(exposed, customer_id, NULL)), COUNT(DISTINCT customer_id)) AS exposure_rate,
       COUNTIF(exposure_count > 1) AS repeated_exposure_rows,
       COUNTIF(converted AND NOT exposed) AS converted_without_exposure,
       COUNT(DISTINCT customer_id) AS itt_denominator
FROM assigned
GROUP BY variant ORDER BY variant;

