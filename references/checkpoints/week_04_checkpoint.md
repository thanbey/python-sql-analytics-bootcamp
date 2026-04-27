# Week 4 Checkpoint — Window Functions + CTEs

## Week Summary
Week 4 covered the most powerful SQL constructs for analytics work: window functions and Common Table Expressions (CTEs). You learned `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, `SUM() OVER`, `AVG() OVER`, and `PERCENT_RANK()` — all with `PARTITION BY` and `ORDER BY` clauses. You also learned to write CTEs with `WITH name AS (...)` syntax, including multi-CTE queries that chain results. The critical distinction between `GROUP BY` (which collapses rows) and `PARTITION BY` (which keeps all rows while adding a group-level value) became clear through benchmarking exercises.

---

## Must-Know Skills
I can…

1. Write `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` to rank rows within a group
2. Explain the difference between ROW_NUMBER, RANK, and DENSE_RANK (RANK skips numbers after ties; DENSE_RANK does not)
3. Use `LAG(col, 1)` and `LEAD(col, 1)` to access the previous/next row's value within a partition
4. Write a running total using `SUM(col) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`
5. Write a moving average using `AVG(col) OVER (... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`
6. Write a CTE with `WITH name AS (SELECT ...)` and reference it in the main query
7. Write a multi-CTE query where CTE2 references CTE1
8. Explain why `PARTITION BY` preserves row count while `GROUP BY` reduces it — and when you need each
9. Use `PERCENT_RANK()` and `CUME_DIST()` to assign percentile ranks
10. Write a top-N-per-group query using a CTE with `ROW_NUMBER()` then `WHERE rn <= N`

---

## Self-Test Tasks

**Task 1:** Write a SQL query that adds a column to `bw_sales_kpis` showing each row's revenue as a percentage of the total revenue for that month (`CAL_YEAR_MONTH`). Do not use a subquery — use a window function.
```sql
-- Write your solution here
```

**Task 2:** Write a CTE-based query that finds the top 2 customers by revenue within each sales org (`VKORG`). Return VKORG, KUNNR, total revenue, and rank.
```sql
-- Write your solution here
```

**Task 3:** Write a query using `LAG()` to show each cost center's actual spend for the current period and the prior period, along with the month-over-month change. Use `cost_center_actuals`, fiscal year 2024.
```sql
-- Write your solution here
```

---

## Pass Criteria

**Passing:**
- Task 1 uses `SUM(REVENUE) OVER (PARTITION BY CAL_YEAR_MONTH)` in the denominator — no GROUP BY needed
- Task 2 CTE uses `ROW_NUMBER() OVER (PARTITION BY VKORG ORDER BY SUM(REVENUE) DESC)` and the outer query filters `WHERE rn <= 2`
- Task 3 uses `LAG(SUM(ACTUAL_AMT)) OVER (PARTITION BY KOSTL ORDER BY PERIOD)` with correct GROUP BY in a CTE first
- All three queries return correct row counts (Task 1 has same rows as bw_kpis; Task 2 has ≤ 2 rows per VKORG)

**Needs More Work:**
- Task 1: tried to use GROUP BY instead of window function — GROUP BY would collapse to one row per month, losing the per-row detail
- Task 2: got the right idea but LAG applied before grouping caused wrong results — remember: aggregate first in a CTE, then apply window functions
- Task 3: used ROW_NUMBER where you needed DENSE_RANK, causing ties to be lost

---

## Carry-Forward Items

1. **Aggregate before windowing** — window functions operate on the result of GROUP BY, not on raw rows. When you need both, use a CTE to aggregate first, then apply window functions in the outer query. This trips up even experienced SQL writers.
2. **ROWS vs RANGE in window frames** — `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` is a physical row count. `RANGE BETWEEN INTERVAL '2' MONTH PRECEDING AND CURRENT ROW` is a value-based range (date-aware). The RANGE form matters for time-series analysis with gaps in the data.
3. **NULL in LAG/LEAD** — the first row in a partition has no LAG value — it returns NULL. Always use `COALESCE(LAG(col), 0)` or handle it in your output formatting.

---

## Relevant SAP/Analytics Context

Window functions are the SQL equivalent of SAP BW Calculated Key Figures with "Exception Aggregation" and "Cumulation" settings. The `LAG()` function replicates what BEx does when you compare a key figure to the "previous period" using time-relative key figures. The top-N-per-group CTE pattern is equivalent to filtering a BW report to show only the top 5 customers — except the SQL version is fully reproducible and explainable. In SAP HANA Calculation Views, window functions are used extensively in analytic privileges and in the "calculated column" layer of Graphical Calculation Views. Mastering these patterns makes you effective in both worlds.
