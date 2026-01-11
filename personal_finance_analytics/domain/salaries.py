import logging
import pandas as pd

from personal_finance_analytics.utils import Settings

from .exceptions import SalariesSpreadsheetException


def get_salaries_csv() -> pd.DataFrame:
    try:
        return pd.read_csv(  # type: ignore
            f"https://docs.google.com/spreadsheets/d/{Settings.SALARIES_SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=2020"
        )
    except Exception as e:
        logging.error("Error reading salaries CSV: %s", e)
        raise SalariesSpreadsheetException("Failed to read salaries CSV") from e


def get_current_month_salary() -> float:
    df = get_salaries_csv()
    last_salary = df["sueldo_neto_ars"].iloc[-1]
    return float(last_salary)


def get_adjusted_salaries(INFLATION_SINCE_LAST_PROMOTION: bool = True) -> pd.DataFrame:
    datos_personales = get_salaries_csv()
    datos_personales["sueldo_ajustado"] = datos_personales["sueldo_neto_ars"].iloc[0]

    for i in range(1, len(datos_personales)):
        if (
            datos_personales.loc[i, "puesto"] != datos_personales.loc[i - 1, "puesto"]
            or datos_personales.loc[i, "seniority"]
            != datos_personales.loc[i - 1, "seniority"]
        ) and INFLATION_SINCE_LAST_PROMOTION:
            datos_personales.loc[i, "sueldo_ajustado"] = datos_personales.loc[
                i - 1, "sueldo_ajustado"
            ] + (
                datos_personales.loc[i, "sueldo_neto_ars"]
                - datos_personales.loc[i - 1, "sueldo_neto_ars"]
            )
        elif datos_personales.loc[i, "puesto"] != None:
            datos_personales.loc[i, "sueldo_ajustado"] = datos_personales.loc[
                i - 1, "sueldo_ajustado"
            ] * (1 + datos_personales.loc[i, "inflacion_del_mes_anterior"] / 100)
        else:
            datos_personales.loc[i, "sueldo_ajustado"] = 0.00

    return datos_personales["sueldo_ajustado"]


def get_last_adjusted_salary() -> float:
    last_salary = get_adjusted_salaries()
    return float(last_salary.iloc[-1])


def get_personal_delta() -> str:
    personal_adjusted_salary = float(get_adjusted_salaries(INFLATION_SINCE_LAST_PROMOTION=False).iloc[-1])
    last_salary = get_current_month_salary()
    return f"{((last_salary * 100) / personal_adjusted_salary) - 100:.2f} % from first salary adjusted ($ {personal_adjusted_salary:,.0f}) to current salary ($ {get_current_month_salary():,.0f})"
