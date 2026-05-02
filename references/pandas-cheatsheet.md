# Pandas Cheat Sheet

A quick reference for the pandas patterns used most across this bootcamp. The first
sections are the **general 80/20** of pandas data analysis. The later sections are
**bootcamp-specific**: the SAP CSV layout, the `analytics_bootcamp` helpers, and the
DuckDB round-trip workflow.

```python
import pandas as pd
import numpy as np
```

---

## 1. Load / save

```python
df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", parse_dates=["date_col"], dtype={"id": "Int64"})

df.to_csv("out.csv", index=False)
df.to_parquet("out.parquet", index=False)
```

Bootcamp-style robust CSV load (handles dirty SAP exports — see §11):

```python
df = pd.read_csv("data/raw/sales_orders.csv")
for c in df.select_dtypes("object").columns:
    df[c] = df[c].str.strip()
df["NETWR"] = pd.to_numeric(df["NETWR"], errors="coerce")
df["ERDAT"] = pd.to_datetime(df["ERDAT"], errors="coerce")
```

---

## 2. Inspect

```python
df.head()
df.tail()
df.info()
df.describe()                  # numeric summary
df.describe(include="object")  # categorical summary
df.shape                       # (rows, cols)
df.columns.tolist()
df.dtypes

df["col"].value_counts()
df["col"].value_counts(normalize=True)   # proportions
df["col"].unique()
df["col"].nunique()

df.isna().sum()                # null counts per column
df.duplicated().sum()          # dupe row count
```

---

## 3. Selecting columns and rows

```python
df["col"]                      # Series
df[["col1", "col2"]]           # subset of columns

# by position
df.iloc[0]                     # first row
df.iloc[0:5]                   # first 5 rows
df.iloc[:, 0:3]                # first 3 columns

# by label
df.loc[0]                      # row with index label 0
df.loc[0:10, ["col1", "col2"]]
```

---

## 4. Boolean filtering

This is the dominant filter style in the bootcamp — prefer it over `.filter()` or `.query()`.

```python
df[df["col"] > 0]
df[(df["a"] > 0) & (df["b"] == "x")]
df[df["col"].isin(["a", "b"])]

df[df["col"].isna()]
df[df["col"].notna()]

df[df["col"].between(10, 20)]

# string filters
df[df["MAKTX"].str.contains("PUMP", case=False, na=False)]
df[df["MAKTX"].str.startswith("RAW")]

# query() works too — handy for quick interactive use
df.query("NETWR > 0 and VKORG == '1000'")
```

---

## 5. Create / modify columns

```python
df["c"] = df["a"] + df["b"]
df["flag"] = (df["a"] > 0).astype(int)

df["col"] = df["col"].fillna(0)
df["col"] = df["col"].replace({"old": "new"})

df = df.drop(columns=["unneeded"])
df = df.rename(columns={"old_name": "new_name"})

# chainable style — bootcamp prefers explicit chained calls over .pipe()
df2 = (
    df
    .assign(INV_VALUE=lambda d: d["LABST"] * d["STPRS"])
    .drop(columns=["LABST", "STPRS"])
)
```

**Conditional / bucketed columns** with `np.select` (used for aging buckets):

```python
days = (pd.Timestamp.today() - df["LAST_MOVEMENT_DATE"]).dt.days
conditions = [days <= 30, days <= 90, days <= 180]
choices    = ["Current", "Slow", "Stagnant"]
df["AGING_BUCKET"] = np.select(conditions, choices, default="Dead")
```

---

## 6. Groupby & aggregation

**Named aggregation is the bootcamp standard** — readable and gives clean column names.

```python
g = df.groupby("VKORG")

# quick one-off
g["NETWR"].mean()
g["NETWR"].agg(["mean", "sum", "count"])

# named aggregation (preferred)
sales_by_org = (
    df
    .groupby("VKORG")
    .agg(
        revenue   =("NETWR", "sum"),
        orders    =("VBELN", "nunique"),
        avg_order =("NETWR", "mean"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

# multi-key groupby
df.groupby(["VKORG", "SPART"]).agg(revenue=("NETWR", "sum"))

# per-row group stat (same length as df)
df["org_avg"] = df.groupby("VKORG")["NETWR"].transform("mean")
df["pct_of_org"] = df["NETWR"] / df["org_avg"]
```

**Compute derived columns *before* groupby** rather than using `.apply` inside `.agg` —
faster and clearer:

```python
df["INV_VALUE"] = df["LABST"] * df["STPRS"]
df.groupby("WERKS").agg(total_value=("INV_VALUE", "sum"))
```

---

## 7. Joins / combining

```python
# left join is the default in this repo (lookup masters onto fact tables)
df_merged = pd.merge(sales, materials, on="MATNR", how="left")

# different key names
pd.merge(sales, customers, left_on="KUNNR", right_on="customer_id", how="left")

# stack rows
pd.concat([df1, df2], axis=0, ignore_index=True)

# stack columns (rare — usually you should merge instead)
pd.concat([df1, df2], axis=1)
```

---

## 8. Reshape: wide ↔ long

```python
# long -> wide
pivot = df.pivot_table(
    index="MATNR",
    columns="WERKS",
    values="LABST",
    aggfunc="sum",
    fill_value=0,
)

# wide -> long
long = df.melt(
    id_vars=["MATNR"],
    value_vars=["plant_1000", "plant_2000"],
    var_name="plant",
    value_name="qty",
)
```

---

## 9. Index & sort

```python
df = df.set_index("MATNR")
df = df.reset_index(drop=True)

df = df.sort_values(["VKORG", "NETWR"], ascending=[True, False])
df = df.sort_index()
```

---

## 10. Datetime

```python
df["ERDAT"] = pd.to_datetime(df["ERDAT"], errors="coerce")

df["year"]    = df["ERDAT"].dt.year
df["month"]   = df["ERDAT"].dt.month
df["quarter"] = df["ERDAT"].dt.quarter
df["weekday"] = df["ERDAT"].dt.day_name()

# date diff in days (used for aging buckets)
df["days_old"] = (pd.Timestamp.today() - df["LAST_MOVEMENT_DATE"]).dt.days

# resample after setting datetime index
daily_revenue = (
    df.set_index("ERDAT")
      .resample("D")
      .agg(revenue=("NETWR", "sum"))
)
```

**SAP year-month strings** (`"202404"` style — see week 1 notebooks):

```python
df["YEAR"]  = df["CAL_YEAR_MONTH"].astype(str).str[:4].astype("Int64")
df["MONTH"] = df["CAL_YEAR_MONTH"].astype(str).str[4:6].astype("Int64")
```

---

## 11. Robust type coercion (bootcamp style)

SAP exports often arrive as messy strings. The repo-wide pattern is **strip → coerce → fill**:

```python
def clean_load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # strip whitespace from all string columns
    for c in df.select_dtypes("object").columns:
        df[c] = df[c].str.strip()

    # numeric coercion — bad values become NaN instead of crashing
    for c in ["NETWR", "MENGE", "STPRS"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # date coercion
    for c in ["ERDAT", "HIRE_DATE", "LAST_MOVEMENT_DATE"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    return df
```

**Ordered categorical** for ranked buckets (so groupby/sort respects the order):

```python
aging_order = pd.CategoricalDtype(
    categories=["Current", "Slow", "Stagnant", "Dead"],
    ordered=True,
)
df["AGING_BUCKET"] = df["AGING_BUCKET"].astype(aging_order)
```

---

## 12. Bootcamp datasets (`data/raw/`)

| File | Grain | Key columns |
|---|---|---|
| `bw_sales_kpis.csv` | Aggregated KPI fact | CAL_YEAR_MONTH, VKORG, MATNR, KUNNR, REVENUE, QUANTITY, COGS, GROSS_MARGIN |
| `sales_orders.csv` | Order line item | VBELN, POSNR, KUNNR, MATNR, ERDAT, NETWR, MENGE, VKORG |
| `materials_inventory.csv` | Material × plant × storage | MATNR, MAKTX, WERKS, LGORT, LABST, STPRS, LAST_MOVEMENT_DATE |
| `cost_center_actuals.csv` | Cost center × period | BUKRS, KOSTL, GJAHR, PERIOD, KSTAR, ACTUAL_AMT, PLAN_AMT |
| `hr_headcount.csv` | Employee master | PERNR, ENAME, ORGEH, WERKS, HIRE_DATE, TERM_DATE, SALARY, KOSTL |

---

## 13. `analytics_bootcamp` helpers

Prefer these wrappers over re-implementing CSV loading and cleanup in each notebook.

```python
from analytics_bootcamp import dataset, utils, duckdb_utils

# Loaders — return cleaned DataFrames with stripped strings + correct dtypes
materials = dataset.load_materials()
sales     = dataset.load_sales_orders()
costs     = dataset.load_cost_centers()
hr        = dataset.load_headcount()
kpis      = dataset.load_bw_kpis()

# Batch load — dict of all 5 frames
frames = dataset.load_all()
materials = frames["materials"]

# Analytical wrappers
aging  = utils.inventory_aging_report(materials, plant="1000")
dq     = utils.run_dq_checks(frames)
budget = utils.variance_summary(costs)
```

---

## 14. DuckDB ↔ pandas round-trip

Use DuckDB for heavy joins / window functions, then pull results back into pandas for
charting or export:

```python
from analytics_bootcamp import duckdb_utils

con = duckdb_utils.get_connection()   # registers raw CSVs as views

top_customers = duckdb_utils.query_df("""
    SELECT KUNNR, SUM(NETWR) AS revenue
    FROM sales_orders
    GROUP BY KUNNR
    ORDER BY revenue DESC
    LIMIT 10
""")

# top_customers is a regular pandas DataFrame — chart it, merge it, export it
top_customers.plot.bar(x="KUNNR", y="revenue")
```

Going the other way — register a pandas frame as a DuckDB table:

```python
con.register("my_df", df)
con.execute("SELECT COUNT(*) FROM my_df").df()
```

---

## 15. Export to Tableau

```python
from analytics_bootcamp import tableau

tableau.to_hyper(top_customers, "output/top_customers.hyper")
```

---

## 16. Quick troubleshooting

| Symptom | Fix |
|---|---|
| `SettingWithCopyWarning` | Use `.loc[mask, "col"] = value` instead of chained assignment, or `.copy()` the slice first |
| Merge silently drops rows | Use `how="left"` and check `df.merge(..., indicator=True)["_merge"].value_counts()` |
| Numeric column comes in as `object` | `pd.to_numeric(s, errors="coerce")` |
| Date column won't parse | `pd.to_datetime(s, errors="coerce", format="%Y%m%d")` |
| Group sort wrong order | Cast to ordered `CategoricalDtype` (see §11) |
| Sums look wrong after merge | You probably have a many-to-many join — check `df["key"].value_counts()` on both sides |
