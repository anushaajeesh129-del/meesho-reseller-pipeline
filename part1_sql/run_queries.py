import sqlite3
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Monthly revenue by category
query1 = """
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
"""

rows = cur.execute(query1).fetchall()

with open(
    os.path.join(OUTPUT_DIR, "monthly_category_revenue.csv"),
    "w",
    newline=""
) as f:
    writer = csv.writer(f)
    writer.writerow(["month", "category", "revenue", "n_orders"])
    writer.writerows(rows)

print("1. Monthly category revenue:")
for row in rows:
    print(row)


# 2. Region-wise revenue and order count
query2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;
"""

rows = cur.execute(query2).fetchall()

with open(
    os.path.join(OUTPUT_DIR, "region_revenue.csv"),
    "w",
    newline=""
) as f:
    writer = csv.writer(f)
    writer.writerow(["region", "revenue", "n_orders"])
    writer.writerows(rows)

print("\n2. Region revenue:")
for row in rows:
    print(row)


# 3. Top 5 resellers
query3 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

rows = cur.execute(query3).fetchall()

with open(
    os.path.join(OUTPUT_DIR, "top_resellers.csv"),
    "w",
    newline=""
) as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "total_spend"])
    writer.writerows(rows)

print("\n3. Top resellers:")
for row in rows:
    print(row)


# 4. Resellers with no orders
query4 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

rows = cur.execute(query4).fetchall()

with open(
    os.path.join(OUTPUT_DIR, "zero_order_resellers.csv"),
    "w",
    newline=""
) as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "region"])
    writer.writerows(rows)

print("\n4. Zero-order resellers:")
for row in rows:
    print(row)


# 4B. COUNT(*) vs COUNT(order_id)
query4b = """
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS total_rows,
    COUNT(o.order_id) AS order_count
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;
"""

rows = cur.execute(query4b).fetchall()

print("\n4B. COUNT(*) vs COUNT(order_id):")
for row in rows:
    print(row)


# 5. June Delivered AOV
query5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS aov
FROM orders
WHERE month = 'June'
AND status = 'Delivered';
"""

rows = cur.execute(query5).fetchall()

with open(
    os.path.join(OUTPUT_DIR, "june_delivered_aov.csv"),
    "w",
    newline=""
) as f:
    writer = csv.writer(f)
    writer.writerow(["aov"])
    writer.writerows(rows)

print("\n5. June Delivered AOV:")
for row in rows:
    print(row)


conn.close()

print("\nAll Part 1 queries completed successfully!")