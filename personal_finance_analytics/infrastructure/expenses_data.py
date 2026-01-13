import logging
import pandas as pd

from personal_finance_analytics.utils import ExpensesSpreadsheetException


def get_expenses_data(url: str, cols: list[str] | None = None) -> pd.DataFrame:
    try:
        df = pd.read_csv(url, usecols=cols)
    except Exception as e:
        logging.error(f"Error reading CSV from {url}: {e}")
        raise ExpensesSpreadsheetException(f"Failed to read CSV from {url}") from e
    return df
