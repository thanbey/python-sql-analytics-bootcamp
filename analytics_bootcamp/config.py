"""
config.py — Central configuration for dataset paths and shared constants.

Usage in notebooks:
    from analytics_bootcamp.config import RAW_DATA_DIR, DATASETS

    import pandas as pd
    df = pd.read_csv(DATASETS["materials"])
"""

from pathlib import Path

# ── Repository root (two levels up from this file) ─────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[1]

# ── Data directories (CCDS v2 convention) ──────────────────────────────────
DATA_DIR       = REPO_ROOT / "data"
RAW_DATA_DIR   = DATA_DIR / "raw"
INTERIM_DIR    = DATA_DIR / "interim"
PROCESSED_DIR  = DATA_DIR / "processed"
EXTERNAL_DIR   = DATA_DIR / "external"

# ── Reports / figures ───────────────────────────────────────────────────────
REPORTS_DIR = REPO_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# ── Notebooks ───────────────────────────────────────────────────────────────
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"

# ── Dataset shortcuts ───────────────────────────────────────────────────────
# Use these in any notebook instead of hardcoding relative paths:
#   pd.read_csv(DATASETS["materials"])
DATASETS = {
    "materials":    RAW_DATA_DIR / "materials_inventory.csv",
    "sales_orders": RAW_DATA_DIR / "sales_orders.csv",
    "cost_centers": RAW_DATA_DIR / "cost_center_actuals.csv",
    "headcount":    RAW_DATA_DIR / "hr_headcount.csv",
    "bw_kpis":      RAW_DATA_DIR / "bw_sales_kpis.csv",
}

# ── SAP field reference constants ───────────────────────────────────────────
PLANTS        = ["1000", "2000", "3000"]
SALES_ORGS    = ["1000", "2000"]
DIST_CHANNELS = ["10", "20"]
DIVISIONS     = ["00", "10", "20"]
COMPANY_CODES = ["1000", "2000"]

MATERIAL_TYPES = {
    "ROH":  "Raw Material",
    "HALB": "Semi-Finished",
    "FERT": "Finished Goods",
}

MRP_TYPES = {
    "PD":  "MRP (Deterministic)",
    "VB":  "Reorder Point",
    "ND":  "No MRP",
}

ORDER_STATUSES = ["OPEN", "DELIVERED", "CANCELLED", "BLOCKED"]
