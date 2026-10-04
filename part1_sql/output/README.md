# Part 1 Output: Zero-Order Reseller Analysis

For reseller RS024 (the only reseller with zero orders in the dataset), we must demonstrate why COUNT(*) cannot be used to detect the zero-match case after a LEFT JOIN.

- **COUNT(*) returns 1:** After a LEFT JOIN, the unmatched row for RS024 still exists in the result set, just filled with NULLs for order columns. COUNT(*) counts this physical row, returning 1 (which incorrectly suggests RS024 has an order).
- *COUNT(order_id) returns 0:* This function counts only non-NULL values in the order_id column. Since order_id is NULL for RS024, it correctly returns 0.

Therefore, COUNT(order_id) (or a WHERE order_id IS NULL filter) is the correct way to identify resellers with no orders.