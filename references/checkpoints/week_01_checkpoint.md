# Week 1 Checkpoint — pandas Fundamentals + Data Loading

## Week Summary
Week 1 introduced the core pandas toolkit for loading and inspecting data. You learned to read CSV files, inspect DataFrames (`.head()`, `.info()`, `.describe()`), handle missing values, filter rows with boolean indexing, select columns, and perform basic groupby aggregations. You also loaded all five SAP-style datasets and understood their structure: materials inventory (MATNR/WERKS/STPRS), sales orders (VBELN/NETWR/STATUS), cost center actuals (KOSTL/KSTAR/ACTUAL_AMT/PLAN_AMT), HR headcount (PERNR/ORGEH/SALARY), and the BW KPI extract (CAL_YEAR_MONTH/REVENUE/GROSS_MARGIN).

---

## Must-Know Skills
I can…

1. Load a CSV with `pd.read_csv()` and specify `parse_dates`, `dtype`, and `encoding` parameters
2. Inspect a DataFrame with `.shape`, `.dtypes`, `.info()`, `.describe()`, `.head()`, `.tail()`
3. Filter rows using boolean indexing: `df[df['col'] > value]` and multi-condition filters with `&` and `|`
4. Select columns by name: `df['col']` and `df[['col1','col2']]`
5. Rename columns with `.rename(columns={...})`
6. Identify and count missing values with `.isna().sum()`
7. Fill or drop missing values: `.fillna()` and `.dropna()`
8. Perform basic aggregations: `.groupby('col').agg({'col2': 'sum'})` and `.value_counts()`
9. Sort a DataFrame: `.sort_values('col', ascending=False)`
10. Check unique values in a column: `.nunique()` and `.unique()`

---

## Self-Test Tasks
Write these without looking at any reference material:

**Task 1:** Load `materials_inventory.csv`, filter to plant `WERKS == 1000`, and print the total inventory value (LABST × STPRS) for that plant.
```python
# Write your solution here — no peeking
```

**Task 2:** From `sales_orders.csv`, count the number of orders per STATUS, sorted descending.
```python
# Write your solution here
```

**Task 3:** From `hr_headcount.csv`, find all employees with a SALARY above $150,000 who have not been terminated (TERM_DATE is null). Print their names and org units.
```python
# Write your solution here
```

---

## Pass Criteria

**Passing:**
- All three self-test tasks complete correctly with no errors
- Task 1 produces a single numeric result (not a DataFrame)
- Task 3 uses `.isna()` correctly to identify active employees
- Code is readable: no single line longer than 100 characters, meaningful variable names

**Needs More Work:**
- Had to look up the syntax for boolean indexing or `.fillna()`
- Mixed up `&` with `and` in multi-condition filters (this causes a TypeError on Series)
- Couldn't remember `.groupby().agg()` syntax and used a for-loop instead

---

## Carry-Forward Items
Keep practicing these every day for the next 2 weeks:

1. **Multi-condition boolean indexing** — the `&`, `|`, `~` operators with parentheses. Forgetting parentheses is a very common bug: `df[(condition1) & (condition2)]`
2. **`.groupby().agg()` with multiple functions** — e.g., `agg({'NETWR': ['sum','mean','count']})` — this pattern appears constantly in analytics work
3. **`.fillna()` behaviour** — know when you need `.fillna(0)` vs `.fillna(method='ffill')` and when to use `.dropna(subset=[...])`

---

## Relevant SAP/Analytics Context

In SAP reporting, the equivalent of this week's work is extracting data from a BW query or a transaction like MB52 (inventory) or KSB1 (cost center actuals) and opening the result in Excel. In Python, you're doing the same thing but with more flexibility. The MATNR field you're filtering on is the same as selecting a material in a BW query variable. The GROUPBY aggregation replicates what SAP totalling rows do automatically in ALV grid reports. When you join DataFrames next week, you'll replicate the BW InfoObject SID lookup that links characteristics to their text descriptions.
