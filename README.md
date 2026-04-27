# Python & SQL Analytics Bootcamp

A 40-day self-paced bootcamp for getting technically fluent in Python, SQL, and SAP-flavored analytics.

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)

---

## Overview

This repo is a structured, hands-on curriculum for analysts and data professionals who want to build production-grade fluency in Python, SQL, and SAP-style reporting workflows. It pairs daily notebooks with realistic SAP-flavored datasets (materials, sales, cost centers, headcount, BW KPIs) and weekly checkpoints. By the end, you'll be able to build end-to-end analytics pipelines — from raw CSV ingest, through DuckDB SQL, into pandas transformations, and out to Tableau dashboards.

---

## Quick Start

```bash
git clone https://github.com/thanbey/python-sql-analytics-bootcamp
cd python-sql-analytics-bootcamp
make create_environment   # uv venv --python 3.11
make requirements         # uv pip install -r requirements.txt && uv pip install -e .
make jupyter              # launch notebooks/
```

`tableauhyperapi` is optional and only required if you plan to generate `.hyper` extracts for Tableau Public.

---

## Repo Structure

```
python-sql-analytics-bootcamp/
├── analytics_bootcamp/              # Installable Python module
│   ├── __init__.py
│   ├── config.py                    # Paths, constants, dataset registry
│   ├── dataset.py                   # CSV loaders, schema helpers
│   ├── duckdb_utils.py              # DuckDB connection + query helpers
│   ├── tableau.py                   # .hyper extract writers
│   └── utils.py                     # Reusable analytics functions
├── data/
│   ├── raw/                         # 5 SAP-style CSVs
│   │   ├── materials_inventory.csv
│   │   ├── sales_orders.csv
│   │   ├── cost_center_actuals.csv
│   │   ├── hr_headcount.csv
│   │   └── bw_sales_kpis.csv
│   └── tableau/                     # Generated .hyper files (gitignored)
├── notebooks/
│   ├── 0.0-assessment/              # Diagnostic notebooks
│   ├── 1.0-week01-02/               # Days 1–10: Python & pandas
│   ├── 2.0-week03-04/               # Days 11–20: SQL with DuckDB
│   ├── 3.0-week05-06/               # Days 21–30: SAP analytics projects
│   ├── 4.0-week07-08/               # Days 31–40: Pipelines & interview drills
│   ├── 5.0-databricks/              # SAP-Databricks reference
│   └── 6.0-tableau/                 # Tableau dashboard notebooks
├── references/
│   └── checkpoints/                 # Weekly self-grading rubrics
├── reports/
│   └── figures/                     # Exported plots and charts
├── scripts/
│   └── generate_hyper_files.py      # Batch .hyper extract generation
├── Makefile
├── pyproject.toml
└── requirements.txt
```

---

## Notebook Sections

| Section | Days | Focus |
|---|---|---|
| 0.0 Assessment | — | Diagnostic: Python, SQL, SAP data literacy |
| 1.0 Week 1–2 | 1–10 | Python & pandas fundamentals |
| 2.0 Week 3–4 | 11–20 | SQL deep dive with DuckDB |
| 3.0 Week 5–6 | 21–30 | SAP analytics projects |
| 4.0 Week 7–8 | 31–40 | Pipelines, integration, interview drills |
| 5.0 Databricks | — | Reference: SAP-Databricks patterns, PySpark translation, Medallion architecture |
| 6.0 Tableau | — | .hyper extract generation, dashboard design for Tableau Public |

---

## Key Tools & Stack

| Tool | Role |
|---|---|
| pandas | Data cleaning, reshaping, ML-ready outputs |
| DuckDB | Analytical SQL on CSV/Parquet files — replaces SQLite throughout |
| PySpark | Distributed compute reference (Databricks notebooks) |
| tableauhyperapi | Write .hyper extract files for Tableau Public (optional) |
| uv | Fast Python package manager |

---

## Datasets

All sample data lives in `data/raw/`. Field names follow SAP conventions and join cleanly across files via shared keys (`MATNR`, `KUNNR`, `KOSTL`, `WERKS`).

| File | Rows | SAP Equivalent | Key Fields |
|---|---|---|---|
| `materials_inventory.csv` | 400 | MB52 / MMBE | MATNR, WERKS, LABST |
| `sales_orders.csv` | 500 | VA05 / VBAP | MATNR, KUNNR, VKORG |
| `cost_center_actuals.csv` | 480 | KSB1 | KOSTL, KSTAR, GJAHR, PERIO |
| `hr_headcount.csv` | 350 | SAP HCM | PERNR, KOSTL, WERKS |
| `bw_sales_kpis.csv` | 480 | BW InfoCube | CALMONTH, VKORG, NET_SALES |

---

## Make Commands

| Command | What it does |
|---|---|
| `make create_environment` | Create uv virtualenv (Python 3.11) |
| `make requirements` | Install all dependencies |
| `make jupyter` | Launch Jupyter in `notebooks/` |
| `make assess` | Open first assessment notebook |
| `make tableau` | Generate all `.hyper` files to `data/tableau/` |
| `make lint` | Run flake8 |
| `make format` | Run black + isort |
| `make clean` | Remove `.pyc`, `__pycache__`, `.ipynb_checkpoints` |

---

## Python Module

`analytics_bootcamp` is installed as an editable module by `make requirements`, so you can import its helpers from any notebook or script:

```python
from analytics_bootcamp.dataset import load_all
from analytics_bootcamp.duckdb_utils import get_connection, query_df
from analytics_bootcamp.tableau import to_hyper
from analytics_bootcamp.utils import inventory_aging_report, variance_summary
```

---

## Tableau Workflow

End-to-end path from raw CSV to a published Tableau Public dashboard:

1. Run `make tableau` — generates `.hyper` files in `data/tableau/`.
2. Open the Tableau Public desktop app.
3. Connect to a `.hyper` file.
4. Build and publish your dashboard to Tableau Public.

The `6.0-tableau/` notebooks walk through each dashboard step by step.

---

## License

MIT
