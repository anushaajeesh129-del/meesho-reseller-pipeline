--Query 1: Monthly revenue by category
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;

--Query 2: Region-wise revenue
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;

--Query 3: Top 5 resellers
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY
    r.reseller_id,
    r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

--Query 4: Resellers with no orders
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

--SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

--Understand COUNT(*) vs COUNT(order_id)
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS total_rows,
    COUNT(o.order_id) AS order_count
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY
    r.reseller_id,
    r.reseller_name;

--Query 5: June Delivered AOV
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';    