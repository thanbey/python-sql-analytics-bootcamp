"""
Regenerate all Tableau .hyper extract files.
Usage: python scripts/generate_hyper_files.py
       or: make tableau
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from analytics_bootcamp.duckdb_utils import get_connection
from analytics_bootcamp.tableau import to_hyper

OUTPUT_DIR = Path("data/tableau")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    con = get_connection()

    print("Generating BW Sales KPI extract...")
    bw_kpis = con.sql("""
        SELECT
            CAL_YEAR_MONTH,
            VKORG,
            MATNR,
            SUM(REVENUE)      AS total_sales,
            SUM(GROSS_MARGIN) AS total_margin,
            ROUND(SUM(GROSS_MARGIN) / NULLIF(SUM(REVENUE), 0) * 100, 2) AS margin_pct
        FROM bw_kpis
        GROUP BY CAL_YEAR_MONTH, VKORG, MATNR
        ORDER BY CAL_YEAR_MONTH DESC
    """).df()
    to_hyper(bw_kpis, OUTPUT_DIR / "bw_sales_kpis.hyper", "BW_Sales_KPIs")
    print(f"  -> {OUTPUT_DIR / 'bw_sales_kpis.hyper'}")

    print("Generating Cost Center Variance extract...")
    cc_variance = con.sql("""
        SELECT
            KOSTL,
            GJAHR,
            PERIOD,
            KSTAR,
            SUM(ACTUAL_AMT)                AS actual,
            SUM(PLAN_AMT)                  AS plan,
            SUM(ACTUAL_AMT - PLAN_AMT)     AS variance,
            ROUND(
                SUM(ACTUAL_AMT - PLAN_AMT)
                / NULLIF(SUM(PLAN_AMT), 0) * 100, 2
            ) AS variance_pct
        FROM cost_centers
        GROUP BY KOSTL, GJAHR, PERIOD, KSTAR
        ORDER BY KOSTL, GJAHR, PERIOD
    """).df()
    to_hyper(cc_variance, OUTPUT_DIR / "cost_center_variance.hyper", "Cost_Center_Variance")
    print(f"  -> {OUTPUT_DIR / 'cost_center_variance.hyper'}")

    print("Generating Inventory Aging extract...")
    inventory = con.sql("""
        SELECT
            MATNR,
            WERKS,
            LGORT,
            LABST,
            LAST_MOVEMENT_DATE,
            DATEDIFF('day',
                TRY_CAST(LAST_MOVEMENT_DATE AS DATE),
                CURRENT_DATE
            ) AS days_since_movement,
            CASE
                WHEN DATEDIFF('day', TRY_CAST(LAST_MOVEMENT_DATE AS DATE), CURRENT_DATE) <= 30  THEN '0-30'
                WHEN DATEDIFF('day', TRY_CAST(LAST_MOVEMENT_DATE AS DATE), CURRENT_DATE) <= 60  THEN '31-60'
                WHEN DATEDIFF('day', TRY_CAST(LAST_MOVEMENT_DATE AS DATE), CURRENT_DATE) <= 90  THEN '61-90'
                ELSE '90+'
            END AS aging_bucket
        FROM materials
        ORDER BY days_since_movement DESC
    """).df()
    to_hyper(inventory, OUTPUT_DIR / "inventory_aging.hyper", "Inventory_Aging")
    print(f"  -> {OUTPUT_DIR / 'inventory_aging.hyper'}")

    print("Done. All .hyper files written to data/tableau/")


if __name__ == "__main__":
    main()
