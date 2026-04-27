# Week 5 Checkpoint — SAP-Specific Analytics Projects

## Week Summary
Week 5 moved from learning syntax to applying it on real SAP-pattern analysis. You replicated five SAP transaction-level reports in Python: MB52/MMBE-style inventory aging (Day 21), VA05-style sales order backlog analysis (Day 22), KSB1/S_ALR_87013611-style cost center variance report (Day 23), HCM workforce reporting including turnover calculations (Day 24), and a BW flat-extract KPI dashboard (Day 25). Each project required you to interpret SAP field names (MATNR, KOSTL, VKORG, PERNR, CAL_YEAR_MONTH) and translate business questions into pandas + matplotlib code — the core skill of an senior analytics role.

---

## Must-Know Skills
I can…

1. Calculate inventory aging buckets from a LAST_MOVEMENT_DATE column using `pd.cut()` or conditional logic
2. Flag excess stock by calculating sales velocity from order history and comparing to stock on hand
3. Build an open order backlog analysis: filter OPEN orders, calculate age, segment by sales org and age bucket
4. Calculate absolute variance (ACTUAL - PLAN) and variance percentage, and identify top N variance drivers
5. Compute annualized turnover rate: `(terminations in 12m / average headcount) * 100`
6. Perform salary band analysis: median, 25th/75th percentile by job title using `.quantile()`
7. Derive YoY revenue growth from a BW CAL_YEAR_MONTH column: `df['YEAR'] = df['CAL_YEAR_MONTH'] // 100`
8. Build a customer retention flag by comparing KUNNR sets across two years
9. Format a variance report using pandas Styler with `applymap()` for conditional color coding
10. Produce 5 KPI "cards" as formatted text output from computed numeric values

---

## Self-Test Tasks

**Task 1:** From `materials_inventory.csv`, calculate: (a) total inventory value at risk (aging >90 days) by plant, and (b) count of materials where stock exceeds 3 months of sales velocity. Write the complete pandas code — no peeking at Day 21.
```python
# Write your solution here
```

**Task 2:** From `cost_center_actuals.csv`, write a pandas pipeline (no SQL) that produces a YTD variance report for fiscal year 2024 through period 9, sorted by absolute variance descending, with conditional Styler highlighting: red if variance > 10%, green if variance < -5%.
```python
# Write your solution here
```

**Task 3:** From `bw_sales_kpis.csv`, write the pandas code to identify the region with the steepest gross margin decline between 2024 and 2025.
```python
# Write your solution here
```

---

## Pass Criteria

**Passing:**
- Task 1(a): produces a correct plant-level DataFrame (not a scalar) with `WERKS`, `AT_RISK_VALUE` columns
- Task 1(b): correctly uses `sales_orders.csv` to compute velocity, handles materials with no sales history (velocity = 0, months on hand = inf)
- Task 2: Styler renders with color, numbers are formatted as `$X,XXX`, variance % is correct
- Task 3: produces a single region name with its 2024 GM%, 2025 GM%, and the delta

**Needs More Work:**
- Task 1 calculated inventory value using only LABST without multiplying by STPRS (common oversight)
- Task 2 used `.style.apply()` (row-wise) instead of `.style.applymap()` (element-wise) for a single-column format
- Task 3 sorted by the wrong column (revenue instead of GM%) — re-read the question

---

## Carry-Forward Items

1. **Sales velocity calculation** — always scope the velocity window explicitly (e.g., last 6 months) and handle the zero-velocity case. Materials with no recent sales have infinite months on hand — don't let them silently disappear in a merge.
2. **Styler vs raw output** — pandas Styler only renders in a Jupyter environment. For CSV/Excel export, use conditional formatting in a separate step. Know the difference for delivery format.
3. **BW time characteristics** — `CAL_YEAR_MONTH` is a number (202412), not a string. Always derive YEAR as `// 100` and MONTH as `% 100`. Never use string slicing unless you've already cast to string.

---

## Relevant SAP/Analytics Context

Every project this week directly maps to a SAP report your future clients or colleagues run daily. MB52/MMBE for inventory, VA05 for backlog, KSB1/S_ALR_87013611 for cost center variance — these are among the most-used transactions in SAP. When you arrive at a client engagement and see an analyst exporting these to Excel and manually adding columns, you will be able to say: "I can automate this." That's the value of this week. The KPI dashboard from a BW extract (Day 25) is exactly what SAP Analytics Cloud Story replaces — and knowing how to replicate it in Python means you can validate SAC results independently, which is a high-value skill in audit and advisory contexts.
