"""
Tableau integration utilities for SAP analytics workflows.
Requires: uv pip install tableauhyperapi
"""
try:
    from tableauhyperapi import (
        HyperProcess, Connection, TableDefinition, TableName,
        SqlType, Inserter, CreateMode, Telemetry,
    )
    _HYPER_AVAILABLE = True
except ImportError:
    _HYPER_AVAILABLE = False

import pandas as pd
from pathlib import Path


def _check_hyper():
    if not _HYPER_AVAILABLE:
        raise ImportError(
            "tableauhyperapi is not installed. Run: uv pip install tableauhyperapi"
        )


def pandas_type_to_sql(dtype):
    """Map a pandas dtype to a Tableau SqlType."""
    _check_hyper()
    if pd.api.types.is_integer_dtype(dtype):
        return SqlType.big_int()
    elif pd.api.types.is_float_dtype(dtype):
        return SqlType.double()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return SqlType.timestamp()
    else:
        return SqlType.text()


def to_hyper(df: pd.DataFrame, output_path, table_name: str = "Extract") -> Path:
    """
    Write a pandas DataFrame to a Tableau .hyper extract file.

    Args:
        df: Source DataFrame
        output_path: Path for the .hyper file (e.g. data/tableau/inventory.hyper)
        table_name: Name of the table inside the extract (default: Extract)

    Returns:
        Path to the written .hyper file
    """
    _check_hyper()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cols = [
        TableDefinition.Column(str(col), pandas_type_to_sql(df[col].dtype))
        for col in df.columns
    ]
    table_def = TableDefinition(TableName("Extract", table_name), cols)

    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(
            hyper.endpoint, str(output_path), CreateMode.CREATE_AND_REPLACE
        ) as con:
            con.catalog.create_table(table_def)
            with Inserter(con, table_def) as inserter:
                for row in df.itertuples(index=False):
                    inserter.add_row(list(row))
                inserter.execute()

    return output_path
