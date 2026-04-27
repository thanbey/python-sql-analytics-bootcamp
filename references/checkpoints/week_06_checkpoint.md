# Week 6 Checkpoint — SQL Project Work + Data Quality

## Week Summary
Week 6 applied SQL to production-quality reporting problems. You built month-end close queries (Day 26) including flash reports and accrual anomaly detection, a full DQ check suite with a scorecard DataFrame (Day 27), an end-to-end Python + SQL automated pipeline with modular functions and a CLI (Day 28), 15 medium/hard LeetCode-style SQL problems (Day 29), and the Week 5–6 capstone integrating all datasets into a presentation-ready business review package (Day 30). The emphasis shifted from "can you write the query?" to "can you build something a team would rely on?"

---

## Must-Know Skills
I can…

1. Write a flash report SQL query using conditional aggregation (`SUM(CASE WHEN period = X THEN revenue ELSE 0 END)`) for current, prior month, and prior year comparisons
2. Detect accrual anomalies in SQL: flag periods where actual is less than 50% of the cost center's average
3. Write a comprehensive DQ check suite covering: orphaned records, duplicate PKs, null required fields, referential integrity, and date sanity
4. Build a DQ scorecard DataFrame with `check_name`, `status` (PASS/WARN/FAIL), `record_count`, `failure_count`, `failure_pct`
5. Structure a Python analytics pipeline with modular functions: `load_data()`, `run_dq_checks()`, `calculate_kpis()`, `format_report()`
6. Add type hints and NumPy-style docstrings to all functions
7. Write a gaps-and-islands SQL query using `ROW_NUMBER() - ROW_NUMBER()` group identifier technique
8. Write a SQL median calculation without a MEDIAN() function (using ROW_NUMBER and AVG of middle values)
9. Implement a multi-CTE customer lifetime value tier query (Platinum/Gold/Silver/Bronze)
10. Produce a complete business review package (executive summary + 4 analytical sections) in one notebook

---

## Self-Test Tasks

**Task 1:** Write the SQL flash report query (without looking at Day 26): current month = 202412, prior month = 202411, prior year same = 202312. Columns: KPI name, current month value, prior month value, prior year value. Include at least Revenue, Gross Margin, and Order Count.
```sql
-- Write your solution here
```

**Task 2:** Without looking at Day 27, write a Python function `check_orphaned_records(sales_df, materials_df)` that returns a dict with `{'status': 'PASS'|'WARN'|'FAIL', 'failure_count': N, 'failure_pct': X.XX}`. WARN if <5% orphaned, FAIL if ≥5%.
```python
# Write your solution here
```

**Task 3:** Write a SQL query using two CTEs and at least one window function to find the top 3 cost elements (KSTAR_DESC) by total actual spend in 2024, and show each element's % share of total 2024 spending.
```sql
-- Write your solution here
```

---

## Pass Criteria

**Passing:**
- Task 1: uses `SUM(CASE WHEN ... THEN ... ELSE 0 END)` pattern with UNION ALL for multiple KPIs — correct column names
- Task 2: function handles edge case where `sales_df` has no MATNR column gracefully (at minimum doesn't crash with a KeyError)
- Task 3: uses window function `SUM(total_actual) OVER ()` (no partition = grand total) to compute share %
- All three tasks completed from memory in under 15 minutes total

**Needs More Work:**
- Task 1: used Python/pandas for the flash report instead of SQL — practice the conditional aggregation pattern until it's automatic
- Task 2: didn't handle the WARN vs FAIL threshold logic — re-read the DQ scorecard design
- Task 3: used a subquery instead of a CTE — either works, but CTE is expected at this level

---

## Carry-Forward Items

1. **Conditional aggregation** (`SUM(CASE WHEN...)`) — this is one of the highest-ROI SQL patterns in analytics work. It appears in flash reports, period comparisons, cohort analysis, and attribution. Practice until you can write it automatically.
2. **DQ scorecard pattern** — the `add_check(name, status, total, failures)` accumulator pattern is reusable across every engagement. Keep your Day 27 code as a template you can adapt.
3. **Modular pipeline design** — the `load → validate → calculate → format` pipeline from Day 28 is the right mental model for any automated report. Review your Day 28 code and ask: "Is each function doing exactly one thing?"

---

## Relevant SAP/Analytics Context

The month-end close queries you built this week are the analytical backbone of a Finance function. At enterprise analytics, you would use this exact type of query to validate client financials during an audit or advisory engagement — comparing period actuals to prior periods to identify unusual movements that need explanation. The DQ check suite replicates the validation layer in SAP BW transformation rules (the "routine check" step where SAP rejects records that fail quality criteria before loading them into InfoCubes). The automated pipeline pattern (Day 28) is what you'd build to replace a manually-run monthly report — a common deliverable in analytics transformation projects.
