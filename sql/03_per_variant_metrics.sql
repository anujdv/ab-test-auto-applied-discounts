-- BigQuery Standard SQL. Customer-level metrics; contribution_margin should be Finance-defined.
WITH users AS (
  SELECT *
  FROM `project.dataset.experiment_events`
  WHERE experiment_id = 301
    AND eligible = TRUE
)
SELECT variant,
       COUNT(DISTINCT customer_id) AS assigned_customers,
       SAFE_DIVIDE(COUNT(DISTINCT IF(converted, customer_id, NULL)), COUNT(DISTINCT customer_id)) AS conversion_rate,
       AVG(IF(converted, 1.0, 0.0)) AS conversion_rate_check,
       AVG(revenue) AS revenue_per_eligible_customer,
       SAFE_DIVIDE(SUM(revenue), SUM(order_count)) AS average_order_value,
       AVG(contribution_margin) AS contribution_margin_per_eligible_customer,
       AVG(discount_cost) AS discount_cost_per_eligible_customer,
       AVG(IF(refund, 1.0, 0.0)) AS refund_rate,
       AVG(IF(payment_failed, 1.0, 0.0)) AS payment_failure_rate,
       AVG(IF(support_contact, 1.0, 0.0)) AS support_contact_rate
FROM users GROUP BY variant ORDER BY variant;

