# Product Performance Context

## Business Objective
Understand which products drive revenue and profit, and identify optimization opportunities.

Primary metrics:
- Product Revenue
- Product Profit
- Units Sold
- Conversion Proxy (Sales Volume)
- Top Performing Products
- Underperforming Products
- Category Performance

## Key Tables

### Products
- Contains product attributes and cost
- Primary key: `id`

### Order Items
- Contains transactions and sale prices
- Joins to products via `product_id`

## SQL Metric Definitions

### Revenue by Product
```sql
SELECT
    product_id,
    SUM(sale_price) AS revenue
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY product_id
ORDER BY revenue DESC;
```

### Units Sold
```sql
SELECT
    product_id,
    COUNT(*) AS units_sold
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY product_id;
```

### Product Profit
```sql
SELECT
    oi.product_id,
    SUM(oi.sale_price - p.cost) AS profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
WHERE oi.status NOT IN ('Cancelled', 'Returned')
GROUP BY oi.product_id
ORDER BY profit DESC;
```

### Product Margin
```sql
SELECT
    oi.product_id,
    SUM(oi.sale_price - p.cost) / SUM(oi.sale_price) AS margin
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
WHERE oi.status NOT IN ('Cancelled', 'Returned')
GROUP BY oi.product_id;
```

### Category Performance
```sql
SELECT
    p.category,
    SUM(oi.sale_price) AS revenue,
    SUM(oi.sale_price - p.cost) AS profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
WHERE oi.status NOT IN ('Cancelled', 'Returned')
GROUP BY p.category
ORDER BY revenue DESC;
```

### Underperforming Products (Low Revenue)
```sql
SELECT
    product_id,
    SUM(sale_price) AS revenue
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY product_id
HAVING revenue < 1000
ORDER BY revenue ASC;
```

### Units Sold
```sql
```
