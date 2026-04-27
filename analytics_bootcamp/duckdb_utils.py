"""DuckDB utilities for SAP analytics workflows."""
import duckdb
import pandas as pd
from pathlib import Path
from analytics_bootcamp.config import DATASETS


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return an in-memory DuckDB connection with all SAP tables registered as views."""
    con = duckdb.connect()
    for name, path in DATASETS.items():
        con.execute(f"CREATE VIEW {name} AS SELECT * FROM read_csv_auto('{path}')")
    return con


def query(sql: str, con=None) -> duckdb.DuckDBPyRelation:
    """Run a SQL query. Creates a fresh connection if none provided."""
    if con is None:
        con = get_connection()
    return con.sql(sql)


def query_df(sql: str, con=None) -> pd.DataFrame:
    """Run a SQL query and return results as a pandas DataFrame."""
    return query(sql, con).df()


def load_sap_tables(con=None) -> duckdb.DuckDBPyConnection:
    """Register all SAP CSV files as named DuckDB views. Returns connection."""
    return con or get_connection()
