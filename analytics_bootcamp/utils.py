"""
utils.py — Shared analytics utility functions.

Reusable helpers that appear across multiple notebooks, extracted here so
notebooks stay clean and code stays DRY.

Usage:
    from analytics_bootcamp.utils import inventory_aging_report, run_dq_checks, load_sqlite_db
"""

import sqlite3
import logging
from datetime import datetime, timezone
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ── Database helpers ─────────────────────────────────────────────────────────

def load_sqlite_db(dataframes: dict[str, pd.DataFrame]) -> sqlite3.Connection:
    """Load a dict of DataFrames into an in-memory SQLite database.

    Table names match the dict keys. Existing tables are replaced.

    Args:
        dataframes: dict mapping table_name → DataFrame

    Returns:
        sqlite3.Connection (in-memory, caller is responsible for closing)

    Example:
        from analytics_bootcamp.dataset import load_all
        from analytics_bootcamp.utils import load_sqlite_db

        conn = load_sqlite_db(load_all())
        pd.read_sql("SELECT COUNT(*) FROM materials", conn)
    """
    conn = sqlite3.connect(":memory:")
    for table_name, df in dataframes.items():
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info("Loaded table '%s' (%d rows, %d cols)", table_name, len(df), len(df.columns))
    return conn


def run_query(conn: sqlite3.Connection, sql: str) -> pd.DataFrame:
    """Execute a SQL query and return results as a DataFrame.

    Args:
        conn: Active sqlite3 connection
        sql:  SQL query string

    Returns:
        pd.DataFrame with query results
    """
    return pd.read_sql_query(sql, conn)


# ── Inventory helpers ────────────────────────────────────────────────────────

def inventory_aging_report(df: pd.DataFrame, plant: str | None = None) -> pd.DataFrame:
    """Categorise materials by days since last movement into aging buckets.

    Aging buckets:
        Current   — ≤ 30 days
        Slow      — 31 to 90 days
        Stagnant  — 91 to 180 days
        Dead      — > 180 days or no movement date recorded

    Args:
        df:    Materials inventory DataFrame (must have LAST_MOVEMENT_DATE, LABST, STPRS, WERKS)
        plant: Optional WERKS code to filter to a single plant

    Returns:
        pd.DataFrame with columns: AGING_BUCKET, MATERIAL_COUNT, TOTAL_VALUE, AVG_DAYS_SINCE_MOVEMENT
    """
    if plant:
        df = df[df["WERKS"] == plant].copy()

    today = pd.Timestamp.now(tz=None).normalize()
    df = df.copy()
    df["DAYS_SINCE_MOVEMENT"] = (today - df["LAST_MOVEMENT_DATE"]).dt.days
    df["INV_VALUE"] = df["LABST"].fillna(0) * df["STPRS"].fillna(0)

    conditions = [
        df["LAST_MOVEMENT_DATE"].isna(),
        df["DAYS_SINCE_MOVEMENT"] > 180,
        df["DAYS_SINCE_MOVEMENT"] > 90,
        df["DAYS_SINCE_MOVEMENT"] > 30,
    ]
    choices = ["Dead", "Dead", "Stagnant", "Slow"]
    df["AGING_BUCKET"] = np.select(conditions, choices, default="Current")

    bucket_order = pd.CategoricalDtype(["Current", "Slow", "Stagnant", "Dead"], ordered=True)
    df["AGING_BUCKET"] = df["AGING_BUCKET"].astype(bucket_order)

    return (
        df.groupby("AGING_BUCKET", observed=True)
        .agg(
            MATERIAL_COUNT=("MATNR", "count"),
            TOTAL_VALUE=("INV_VALUE", "sum"),
            AVG_DAYS_SINCE_MOVEMENT=("DAYS_SINCE_MOVEMENT", "mean"),
        )
        .reset_index()
        .sort_values("AGING_BUCKET")
    )


# ── Data quality helpers ─────────────────────────────────────────────────────

def run_dq_checks(dataframes: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Run a standard suite of data quality checks across all loaded tables.

    Checks performed:
        - Null analysis on all columns
        - Duplicate row detection
        - Orphaned foreign keys (sales_orders.MATNR → materials)
        - Date sanity (TERM_DATE before HIRE_DATE in headcount)

    Args:
        dataframes: dict mapping table_name → DataFrame (use load_all())

    Returns:
        pd.DataFrame — DQ scorecard with columns:
            CHECK_NAME, TABLE, COLUMN, STATUS, RECORD_COUNT, FAILURE_COUNT, FAILURE_PCT, NOTES
    """
    results: list[dict[str, Any]] = []

    def _add(check, table, column, total, failures, notes=""):
        pct = round(failures / total * 100, 2) if total > 0 else 0.0
        status = "PASS" if failures == 0 else ("WARN" if pct < 5 else "FAIL")
        results.append({
            "CHECK_NAME": check,
            "TABLE": table,
            "COLUMN": column,
            "STATUS": status,
            "RECORD_COUNT": total,
            "FAILURE_COUNT": failures,
            "FAILURE_PCT": pct,
            "NOTES": notes,
        })

    for name, df in dataframes.items():
        n = len(df)

        # Null checks
        for col in df.columns:
            nulls = df[col].isna().sum()
            _add("NULL_CHECK", name, col, n, int(nulls))

        # Duplicate rows
        dups = df.duplicated().sum()
        _add("DUPLICATE_ROWS", name, "(all columns)", n, int(dups))

    # Referential integrity: sales_orders.MATNR → materials.MATNR
    if "sales_orders" in dataframes and "materials" in dataframes:
        so = dataframes["sales_orders"]
        mat = dataframes["materials"]
        valid_matnrs = set(mat["MATNR"].dropna())
        orphans = (~so["MATNR"].isin(valid_matnrs)).sum()
        _add("REF_INTEGRITY", "sales_orders", "MATNR → materials.MATNR",
             len(so), int(orphans), "Orders with no matching material master record")

    # Date sanity: headcount TERM_DATE must be >= HIRE_DATE
    if "headcount" in dataframes:
        hc = dataframes["headcount"]
        termed = hc.dropna(subset=["TERM_DATE", "HIRE_DATE"])
        bad_dates = (termed["TERM_DATE"] < termed["HIRE_DATE"]).sum()
        _add("DATE_SANITY", "headcount", "TERM_DATE >= HIRE_DATE",
             len(termed), int(bad_dates), "Employees with termination before hire date")

    return pd.DataFrame(results)


# ── Reporting helpers ────────────────────────────────────────────────────────

def variance_summary(df: pd.DataFrame,
                     actual_col: str = "ACTUAL_AMT",
                     plan_col: str = "PLAN_AMT") -> pd.DataFrame:
    """Add variance columns to a cost center actuals DataFrame.

    Args:
        df:         Cost center actuals DataFrame
        actual_col: Column name for actual spend
        plan_col:   Column name for planned spend

    Returns:
        Original DataFrame with added columns: VARIANCE, VARIANCE_PCT, OVER_BUDGET
    """
    df = df.copy()
    df["VARIANCE"]     = df[actual_col] - df[plan_col]
    df["VARIANCE_PCT"] = (df["VARIANCE"] / df[plan_col].replace(0, np.nan)) * 100
    df["OVER_BUDGET"]  = df["VARIANCE"] > 0
    return df


def format_currency(value: float, symbol: str = "$") -> str:
    """Format a number as a currency string.

    Examples:
        format_currency(1234567.89)  → '$1,234,567.89'
        format_currency(-500)        → '-$500.00'
    """
    if pd.isna(value):
        return "N/A"
    sign = "-" if value < 0 else ""
    return f"{sign}{symbol}{abs(value):,.2f}"
