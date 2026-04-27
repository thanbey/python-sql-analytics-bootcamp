"""
dataset.py — Data loading helpers.

All functions return cleaned DataFrames ready for analysis.
Each function applies minimal, documented transformations so the raw files
are always treated as immutable (CCDS principle: raw data is read-only).

Usage:
    from analytics_bootcamp.dataset import load_materials, load_all

    materials = load_materials()
    all_data  = load_all()  # returns a dict of DataFrames
"""

import pandas as pd
from analytics_bootcamp.config import DATASETS


# ── Individual loaders ───────────────────────────────────────────────────────

def load_materials() -> pd.DataFrame:
    """Load and lightly clean the materials inventory master.

    Transformations:
        - Parse LAST_MOVEMENT_DATE as datetime
        - Strip whitespace from string columns
        - Cast LABST and STPRS to float

    Returns:
        pd.DataFrame with columns: MATNR, MAKTX, WERKS, LGORT, LABST,
        EINHEIT, STPRS, LAST_MOVEMENT_DATE, MATERIAL_TYPE, MRPTYPE
    """
    df = pd.read_csv(DATASETS["materials"], dtype=str)
    df["LABST"] = pd.to_numeric(df["LABST"], errors="coerce")
    df["STPRS"] = pd.to_numeric(df["STPRS"], errors="coerce")
    df["LAST_MOVEMENT_DATE"] = pd.to_datetime(df["LAST_MOVEMENT_DATE"], errors="coerce")
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()
    return df


def load_sales_orders() -> pd.DataFrame:
    """Load and lightly clean the sales orders extract.

    Transformations:
        - Parse ERDAT as datetime
        - Cast NETWR and MENGE to float
        - Strip whitespace from string columns

    Returns:
        pd.DataFrame with columns: VBELN, POSNR, KUNNR, MATNR, ERDAT,
        NETWR, MENGE, WAERK, VKORG, VTWEG, SPART, STATUS
    """
    df = pd.read_csv(DATASETS["sales_orders"], dtype=str)
    df["ERDAT"] = pd.to_datetime(df["ERDAT"], errors="coerce")
    df["NETWR"] = pd.to_numeric(df["NETWR"], errors="coerce")
    df["MENGE"] = pd.to_numeric(df["MENGE"], errors="coerce")
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()
    return df


def load_cost_centers() -> pd.DataFrame:
    """Load and lightly clean the cost center actuals.

    Transformations:
        - Cast GJAHR and PERIOD to int
        - Cast ACTUAL_AMT and PLAN_AMT to float
        - Strip whitespace from string columns

    Returns:
        pd.DataFrame with columns: BUKRS, KOSTL, KTEXT, GJAHR, PERIOD,
        KSTAR, KSTAR_DESC, ACTUAL_AMT, PLAN_AMT, CURRENCY
    """
    df = pd.read_csv(DATASETS["cost_centers"], dtype=str)
    df["GJAHR"]      = pd.to_numeric(df["GJAHR"], errors="coerce").astype("Int64")
    df["PERIOD"]     = pd.to_numeric(df["PERIOD"], errors="coerce").astype("Int64")
    df["ACTUAL_AMT"] = pd.to_numeric(df["ACTUAL_AMT"], errors="coerce")
    df["PLAN_AMT"]   = pd.to_numeric(df["PLAN_AMT"], errors="coerce")
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()
    return df


def load_headcount() -> pd.DataFrame:
    """Load and lightly clean the HR headcount extract.

    Transformations:
        - Parse HIRE_DATE and TERM_DATE as datetime
        - Cast SALARY to float
        - Derive IS_ACTIVE flag (TERM_DATE is null)
        - Strip whitespace from string columns

    Returns:
        pd.DataFrame with original columns plus IS_ACTIVE (bool)
    """
    df = pd.read_csv(DATASETS["headcount"], dtype=str)
    df["HIRE_DATE"] = pd.to_datetime(df["HIRE_DATE"], errors="coerce")
    df["TERM_DATE"] = pd.to_datetime(df["TERM_DATE"], errors="coerce")
    df["SALARY"]    = pd.to_numeric(df["SALARY"], errors="coerce")
    df["IS_ACTIVE"] = df["TERM_DATE"].isna()
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()
    return df


def load_bw_kpis() -> pd.DataFrame:
    """Load and lightly clean the BW sales KPI fact table.

    Transformations:
        - Parse CAL_YEAR_MONTH into a proper period (stored as string YYYYMM)
        - Cast all numeric KPI columns to float
        - Derive YEAR and MONTH integer columns for easy grouping
        - Strip whitespace from string columns

    Returns:
        pd.DataFrame with original columns plus YEAR (int), MONTH (int)
    """
    numeric_cols = [
        "REVENUE", "QUANTITY", "RETURNS_QTY", "RETURNS_VALUE",
        "COGS", "GROSS_MARGIN", "DISCOUNT_AMT", "NUM_ORDERS",
    ]
    df = pd.read_csv(DATASETS["bw_kpis"], dtype=str)
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["CAL_YEAR_MONTH"] = df["CAL_YEAR_MONTH"].str.strip()
    df["YEAR"]  = df["CAL_YEAR_MONTH"].str[:4].astype("Int64")
    df["MONTH"] = df["CAL_YEAR_MONTH"].str[4:].astype("Int64")
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()
    return df


# ── Bulk loader ──────────────────────────────────────────────────────────────

def load_all() -> dict[str, pd.DataFrame]:
    """Load all five datasets and return as a named dict.

    Usage:
        data = load_all()
        data["materials"].head()

    Returns:
        dict with keys: materials, sales_orders, cost_centers, headcount, bw_kpis
    """
    return {
        "materials":    load_materials(),
        "sales_orders": load_sales_orders(),
        "cost_centers": load_cost_centers(),
        "headcount":    load_headcount(),
        "bw_kpis":      load_bw_kpis(),
    }
