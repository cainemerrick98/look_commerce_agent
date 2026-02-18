/**
Calculates customer lifetime value as total spend across all items
grouped by user id
**/
SELECT 
    user_id, 
    SUM(sale_price) AS total_lifetime_spend,
    COUNT(order_id) AS total_orders,
    MAX(created_at) AS last_purchase_date
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY user_id