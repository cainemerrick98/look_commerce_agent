# Orders & Fulfillment Context

## Business Objective
Understand operational performance, fulfillment efficiency, and order outcomes.

Primary metrics:
- Order Volume
- Fulfillment Status
- Cancellation Rate
- Return Rate
- Shipping Time
- Delivery Performance

## Key Tables

### Orders
- Contains order-level logistics and timestamps
- Primary key: `order_id`

### Order Items
- Contains item-level status and revenue

## SQL Metric Definitions

### Total Orders Over Time
```sql
SELECT
    DATE_TRUNC(DATE(created_at), MONTH) AS month,
    COUNT(DISTINCT order_id) AS total_orders
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY month
ORDER BY month;
```

### Total Orders Over Time
```sql
SELECT
    DATE_TRUNC(DATE(created_at), MONTH) AS month,
    COUNT(DISTINCT order_id) AS total_orders
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY month
ORDER BY month;
```

### Order Status Breakdown
```sql
SELECT
    status,
    COUNT(*) AS order_items
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY status
ORDER BY order_items DESC;
```

### Cancellation Rate
```sql
SELECT
    COUNTIF(status = 'Cancelled') / COUNT(*) AS cancellation_rate
FROM `bigquery-public-data.thelook_ecommerce.order_items`;
```

### Return Rate
```sql
SELECT
    COUNTIF(status = 'Returned') / COUNT(*) AS return_rate
FROM `bigquery-public-data.thelook_ecommerce.order_items`;
```

### Average Shipping Time
```sql
SELECT
    AVG(DATE_DIFF(shipped_at, created_at, DAY)) AS avg_shipping_days
FROM `bigquery-public-data.thelook_ecommerce.orders`
WHERE shipped_at IS NOT NULL;
```

### Delivery Time
```sql
SELECT
    AVG(DATE_DIFF(delivered_at, shipped_at, DAY)) AS avg_delivery_days
FROM `bigquery-public-data.thelook_ecommerce.orders`
WHERE delivered_at IS NOT NULL
AND shipped_at IS NOT NULL;
```