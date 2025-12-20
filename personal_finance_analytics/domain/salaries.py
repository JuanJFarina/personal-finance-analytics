import logging
import pandas as pd
import os

from .exceptions import SalariesSpreadsheetException


def get_salaries_csv() -> pd.DataFrame:
    try:
        return pd.read_csv(  # type: ignore
            f"https://docs.google.com/spreadsheets/d/{os.getenv('SALARIES_SPREADHSEET_ID')}/gviz/tq?tqx=out:csv&sheet=2020"
        )
    except Exception as e:
        logging.error("Error reading salaries CSV: %s", e)
        raise SalariesSpreadsheetException("Failed to read salaries CSV") from e


def get_last_net_salary() -> float:
    df = get_salaries_csv()
    last_salary = df["sueldo_neto_ars"].iloc[-1]
    return float(last_salary)
