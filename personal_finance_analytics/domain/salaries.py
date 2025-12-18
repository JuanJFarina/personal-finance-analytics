import pandas as pd
import os


def get_salaries_csv() -> pd.DataFrame:
    return pd.read_csv(  # type: ignore
        f"https://docs.google.com/spreadsheets/d/{os.getenv('SALARIES_SPREADHSEET_ID')}/gviz/tq?tqx=out:csv&sheet=2020"
    )
