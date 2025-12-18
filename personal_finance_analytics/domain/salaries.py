import pandas as pd
import os


def get_salaries_csv() -> pd.DataFrame:
    return pd.read_csv(  # type: ignore
        f"https://docs.google.com/spreadsheets/d/{os.getenv('SALARIES_SPREADHSEET_ID')}/gviz/tq?tqx=out:csv&sheet=2020"
    )


def get_last_net_salary() -> float:
    df = get_salaries_csv()
    last_salary = df["sueldo_neto_ars"].iloc[-1]
    return float(last_salary)
