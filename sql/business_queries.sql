/* ============================================================
   SUPPLY CHAIN CONTROL TOWER – BUSINESS ANALYSIS QUERIES
   Database: SupplyChain_ControlTower
   ============================================================ */

/* ------------------------------------------------------------
   1. Supplier Delay Performance
   Which suppliers have an average delivery delay > 3 days?
   ------------------------------------------------------------ */

SELECT 
    s.SupplierName,
    AVG(t.Actual_Delivery_Days - t.Promised_Delivery_Days) AS Avg_Delay_Days
FROM Transactions t
JOIN Suppliers s
    ON t.SupplierID = s.SupplierID
WHERE t.Type = 'Purchase'
GROUP BY s.SupplierName
HAVING AVG(t.Actual_Delivery_Days - t.Promised_Delivery_Days) > 3
ORDER BY Avg_Delay_Days DESC;


/* ------------------------------------------------------------
   2. Current Stock Position by Product
   What is the net stock level for each product?
   ------------------------------------------------------------ */

SELECT 
    p.ProductName,
    SUM(CASE WHEN t.Type = 'Purchase' THEN t.Quantity ELSE 0 END)
    -
    SUM(CASE WHEN t.Type = 'Sale' THEN t.Quantity ELSE 0 END) AS Current_Stock
FROM Transactions t
JOIN Products p
    ON t.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY Current_Stock ASC;


/* ------------------------------------------------------------
   3. Inventory Capital Exposure by Category
   Which product categories tie up the most capital?
   ------------------------------------------------------------ */

SELECT 
    p.Category,
    SUM(s.Stock * p.UnitCost) AS Inventory_Value
FROM
(
    SELECT 
        ProductID,
        SUM(CASE WHEN Type = 'Purchase' THEN Quantity ELSE 0 END)
        -
        SUM(CASE WHEN Type = 'Sale' THEN Quantity ELSE 0 END) AS Stock
    FROM Transactions
    GROUP BY ProductID
) s
JOIN Products p
    ON s.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY Inventory_Value DESC;


/* ------------------------------------------------------------
   4. OTIF (On-Time-In-Full) Calculation
   What is the overall OTIF percentage?
   ------------------------------------------------------------ */

SELECT 
    ROUND(
        100.0 *
        SUM(CASE 
                WHEN Type = 'Purchase'
                 AND Actual_Delivery_Days <= Promised_Delivery_Days
                THEN 1 ELSE 0 END
        )
        /
        SUM(CASE WHEN Type = 'Purchase' THEN 1 ELSE 0 END)
    ,2) AS OTIF_Percentage
FROM Transactions;
