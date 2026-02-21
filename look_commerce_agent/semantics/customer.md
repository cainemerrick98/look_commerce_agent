# Customer Analytics Context

## Business Objective
Understand customer behavior, retention, and lifetime value to support growth and marketing decisions.

Primary metrics:
- Customer Count
- New Customers
- Customer Lifetime Value (LTV)
- Purchase Frequency
- Repeat Rate
- Customer Retention
- Churn Risk

## Key Tables

### Users
- Contains customer profile information
- One row per customer
- Primary key: `id`

### Order Items
- Used to calculate purchases and revenue per customer
- Joins to users using `user_id`

## SQL Metric Definitions

### Total Customers
```sql
SELECT
    COUNT(DISTINCT id) AS total_customers
FROM `bigquery-public-data.thelook_ecommerce.users`;
```

### New Customers Over Time
```sql
-- First purchase date per customer
with user_first_purchase as (
    SELECT
        user_id,
        MIN(DATE(created_at)) AS first_purchase_date
    FROM `bigquery-public-data.thelook_ecommerce.order_items`
    WHERE status NOT IN ('Cancelled', 'Returned')
    GROUP BY user_id
)

SELECT
    DATE_TRUNC(first_purchase_date, MONTH) AS month,
    COUNT(*) AS new_customers
FROM user_first_purchase
GROUP BY month
ORDER BY month;
```

### Customer Livetime Value
```sql
-- Total revenue generated per customer
SELECT
    user_id,
    SUM(sale_price) AS lifetime_value
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY user_id;
```

### Purchase Frequency
```sql
SELECT
    user_id,
    COUNT(DISTINCT order_id) AS total_orders
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY user_id;
```

### Repeat Rate
```sql
WITH order_count as (
     SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM `bigquery-public-data.thelook_ecommerce.order_items`
    WHERE status NOT IN ('Cancelled', 'Returned')
    GROUP BY user_id
)
SELECT
    COUNTIF(order_count > 1) / COUNT(*) AS repeat_rate
FROM order_count
```

### Churn Risk
```sql
-- Customers inactive for 60+ days
SELECT
    user_id,
    MAX(DATE(created_at)) AS last_order_date
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY user_id
HAVING DATE_DIFF(CURRENT_DATE(), last_order_date, DAY) > 60;
```