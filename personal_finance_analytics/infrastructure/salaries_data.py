import logging
import pandas as pd

from personal_finance_analytics.utils import SalariesSpreadsheetException, Settings


def get_salaries_data() -> pd.DataFrame:
    try:
        return pd.read_csv(  # type: ignore
            f"https://docs.google.com/spreadsheets/d/{Settings.SALARIES_SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=2020"
        )
    except Exception as e:
        logging.error("Error reading salaries CSV: %s", e)
        raise SalariesSpreadsheetException("Failed to read salaries CSV") from e
