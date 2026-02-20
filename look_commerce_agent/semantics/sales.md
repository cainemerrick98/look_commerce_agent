# Sales Context

## Business Objective
Understand how revenue changes over time and identify growth or decline drivers.

Primary metrics:
- Profit per order item
- Total Profit
- Margin (%)
- Total Revenue
- Orders
- Average Order Value (AOV)
- Revenue Growth

## Key Tables

### Order Items
- Contains the sale price of each order item (revenue)

### Product
- Contains the cost of the product to the business. Joins to order items on `product_id`

## SQL Metric Definitions

### Profit per Order Item
```sql
SELECT
    oi.order_id,
    oi.product_id,
    oi.sale_price,
    p.cost,
    (oi.sale_price - p.cost) AS profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
WHERE oi.status NOT IN ('Cancelled', 'Returned');
```

### Total Profit
```sql
-- Sum of profit across all order items
SELECT
    SUM(oi.sale_price - p.cost) AS total_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
WHERE oi.status NOT IN ('Cancelled', 'Returned');
```

### Margin
```sql
-- Portion of revenue that is profit
SELECT
    SUM(oi.sale_price - p.cost) / SUM(oi.sale_price) AS profit_margin
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
WHERE oi.status NOT IN ('Cancelled', 'Returned');
```


### Total Revenue
```sql
-- Sum of all order item sale prices where status is not 'Cancelled' or 'Returned'
SELECT
    SUM(oi.sale_price)
FROM bigquery-public-data.thelook_ecommerce.order_items oi
WHERE oi.status NOT IN ('Cancelled', 'Returned')
```

### Total Orders
```sql
-- Count of unique completed orders
SELECT
    COUNT(DISTINCT oi.order_id) AS total_orders
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
WHERE oi.status NOT IN ('Cancelled', 'Returned');
```

### Average Order Value (AOV)
```sql
-- Revenue divided by number of completed orders
SELECT
    SUM(oi.sale_price) / COUNT(DISTINCT oi.order_id) AS average_order_value
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
WHERE oi.status NOT IN ('Cancelled', 'Returned');
```

### Revenue Over Time
```sql
-- Monthly revenue trend
SELECT
    DATE_TRUNC(DATE(oi.created_at), MONTH) AS month,
    SUM(oi.sale_price) AS revenue
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
WHERE oi.status NOT IN ('Cancelled', 'Returned')
GROUP BY month
ORDER BY month;
```