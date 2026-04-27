# Week 2 Checkpoint — Transformation, Reshaping, and Visualization

## Week Summary
Week 2 focused on transforming and reshaping DataFrames for analytical use. You learned to merge DataFrames (inner, left, right, outer joins), pivot data with `pivot_table()` and `melt()`, apply functions with `.apply()` and `.transform()`, create derived columns, work with string and date columns via the `.str` and `.dt` accessors, and build basic visualizations using matplotlib and a first look at pandas Styler for formatted output. You also encountered the SettingWithCopyWarning and learned the correct pattern (`.copy()`) for safe DataFrame modification.

---

## Must-Know Skills
I can…

1. Merge two DataFrames with `pd.merge()`, specifying `on=`, `how=`, and `left_on=/right_on=` when column names differ
2. Explain the difference between inner, left, and outer joins — and identify when a join will produce fanout (row duplication)
3. Use `.pivot_table()` to create a 2D summary with `index=`, `columns=`, `values=`, `aggfunc=`
4. Use `.melt()` to unpivot a wide DataFrame into a long format
5. Create derived columns with `.assign()` or direct assignment: `df['new_col'] = expression`
6. Use `.apply()` with a lambda for row-wise transformations; use `.transform()` to add a group-level metric back to individual rows
7. Parse and manipulate dates with `.dt.year`, `.dt.month`, `.dt.days`, `pd.to_datetime()`
8. Use string methods: `.str.upper()`, `.str.contains()`, `.str.extract()`, `.str.replace()`
9. Create a bar chart and line chart with matplotlib, with labelled axes and a title
10. Use `pd.cut()` to create binned categories from a numeric column

---

## Self-Test Tasks

**Task 1:** Join `materials_inventory.csv` to `sales_orders.csv` on MATNR. After the join, calculate the total NETWR (order value) per MAKTX (material description). Which material has the highest total order value?
```python
# Write your solution here
```

**Task 2:** From `bw_sales_kpis.csv`, pivot a table showing total REVENUE by REGION (rows) and YEAR (columns). Derive YEAR from `CAL_YEAR_MONTH // 100`.
```python
# Write your solution here
```

**Task 3:** Create a bar chart of headcount by ORGTX (org unit) using `hr_headcount.csv`. Only include active employees (TERM_DATE is null). Title: "Active Headcount by Org Unit".
```python
# Write your solution here
```

---

## Pass Criteria

**Passing:**
- Task 1 produces the correct material name without row duplication (if you see inflated NETWR, you have a fanout problem — fix it)
- Task 2 pivot table has REGION as index, years as columns, no NaN values (use `fill_value=0`)
- Task 3 chart renders without error, has a title, labelled y-axis, and readable x-axis labels

**Needs More Work:**
- Join in Task 1 produced more rows than `sales_orders.csv` has (fanout from non-unique MATNR in materials) — review `how='left'` vs `how='inner'` and check uniqueness before joining
- Task 2: used `.groupby()` correctly but couldn't get to pivot format — review `pivot_table()` docs
- Chart in Task 3 has no axis labels or overlapping tick labels — review `plt.xticks(rotation=45)` and `ax.set_ylabel()`

---

## Carry-Forward Items

1. **Join fanout** — always check: `df.merge(other, on='key').shape[0]` vs `df.shape[0]`. If rows increased, your key isn't unique in the right table. This is the single most common analytics bug.
2. **`.transform()` vs `.apply()`** — apply returns one row per group (collapses); transform returns the same number of rows as input. Practice: "add a column showing each employee's salary as a % of their org unit's total salary" — that requires `.transform()`.
3. **Date arithmetic** — `pd.Timestamp.today() - df['date_col']` returns a Timedelta. Use `.dt.days` to get an integer. Practice calculating tenure in years from HIRE_DATE.

---

## Relevant SAP/Analytics Context

Merging DataFrames in Python is equivalent to using a BW virtual InfoProvider join or an SAP HANA join view. The `how='left'` join corresponds to SAP's "outer left join" in HANA calculation views — keeping all records from the left side regardless of match. The `pivot_table()` output looks exactly like a BEx query with row characteristics (REGION) and column characteristics (YEAR). Understanding this equivalence is critical for translating SAP reporting requests into Python code, which is a core skill for a senior analytics role.
