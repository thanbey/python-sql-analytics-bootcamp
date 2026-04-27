# Week 3 Checkpoint — SQL Foundations + Joins

## Week Summary
Week 3 introduced SQL as a first-class tool alongside pandas. You loaded all five datasets into SQLite using `pandas.to_sql()` and wrote queries using `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, and `LIMIT`. You worked through all four join types (INNER, LEFT, RIGHT, FULL OUTER via UNION), learned the anti-join pattern (LEFT JOIN + WHERE IS NULL), and understood the critical difference between WHERE (pre-aggregation filter) and HAVING (post-aggregation filter). You also learned about NULL behaviour in SQL — that `NULL = NULL` is always false and that aggregate functions silently ignore NULLs.

---

## Must-Know Skills
I can…

1. Load a pandas DataFrame into SQLite with `df.to_sql('table_name', con, if_exists='replace')`
2. Write a `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY` query correctly
3. Explain the difference between WHERE and HAVING and choose the correct one for a given filter
4. Write INNER JOIN, LEFT JOIN, and anti-join queries with correct ON conditions
5. Use aggregate functions: `SUM()`, `COUNT()`, `COUNT(DISTINCT ...)`, `AVG()`, `MIN()`, `MAX()`
6. Use `NULLIF(expr, 0)` to avoid division by zero
7. Use `COALESCE(col, default_value)` to replace NULLs with defaults
8. Use `CASE WHEN ... THEN ... ELSE ... END` for conditional logic in SELECT
9. Use `IS NULL` and `IS NOT NULL` correctly (never `= NULL`)
10. Understand join fanout in SQL: when joining on a non-unique key, rows multiply — always check your counts

---

## Self-Test Tasks

**Task 1:** Write a SQL query that returns total revenue (`NETWR`) and order count by sales org (`VKORG`), but only for sales orgs where total revenue exceeds $500,000. Sort descending by revenue.
```sql
-- Write your solution here
```

**Task 2:** Write a SQL anti-join query that finds all materials in `materials_inventory` that have NO matching rows in `sales_orders`. Return MATNR and MAKTX.
```sql
-- Write your solution here
```

**Task 3:** Write a SQL query that computes, for each cost center (KOSTL) in fiscal year 2024: total actual spend, total planned spend, the variance, and variance as a %. Flag the result 'OVER BUDGET' or 'ON TRACK'. Use `NULLIF` to avoid division by zero.
```sql
-- Write your solution here
```

---

## Pass Criteria

**Passing:**
- Task 1 uses HAVING (not WHERE) to filter after aggregation — using WHERE on an aggregate will produce a syntax error
- Task 2 uses LEFT JOIN + `WHERE m.MATNR IS NULL` pattern, not `NOT IN` (which breaks on NULLs)
- Task 3 computes variance correctly as `ACTUAL - PLAN`, uses NULLIF for division, and CASE WHEN for the flag
- All queries run without error against the SQLite DB

**Needs More Work:**
- Used WHERE to filter on an aggregate function (e.g., `WHERE SUM(NETWR) > 500000`) — this is a syntax error; use HAVING
- Used `WHERE col = NULL` instead of `WHERE col IS NULL` — always 0 rows returned
- Forgot to alias aggregated columns (e.g., `SUM(NETWR) AS total_revenue`) making results hard to read

---

## Carry-Forward Items

1. **NULL trap in joins** — `NOT IN (subquery)` returns zero rows if the subquery contains any NULLs. The anti-join pattern (LEFT JOIN + IS NULL) is always safer. Practice converting a NOT IN to an anti-join.
2. **WHERE vs HAVING** — one rule: if the condition references an aggregate function, it must be in HAVING. Everything else goes in WHERE. Write this rule on a sticky note.
3. **Aggregate functions and NULLs** — `AVG(SALARY)` ignores NULL salaries (denominator = non-null rows). `COUNT(*)` counts all rows including nulls. `COUNT(SALARY)` counts only non-null SALARY values. Know the difference.

---

## Relevant SAP/Analytics Context

The SQL you wrote this week is the foundation of every SAP BW query and HANA view. When you define a BEx query with a "Restricted Key Figure" (e.g., revenue where company code = 1000), that maps to a `SUM(NETWR) WHERE BUKRS = 1000` in SQL. HAVING corresponds to the "Exception Threshold" in BW — values only shown if they meet a condition. The anti-join pattern (find materials with no orders) is exactly what SAP's Missing Data check does in BW validation rules. The NULLIF/COALESCE patterns you learned here appear directly in SAP HANA Calculation View formulas.
