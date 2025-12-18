import os
import pandas as pd

from .months import get_months_until_now, get_next_month
from .salaries import get_last_net_salary

SPREADSHEET_ID = os.getenv("EXPENSES_SPREADHSEET_ID")
NEXT_YEAR_EXPENSES_SPREADHSEET_ID = os.getenv("NEXT_YEAR_EXPENSES_SPREADHSEET_ID")

EXPENSES_GROUPS = {
    "fijos": ["alquileres", "servicios_esenciales", "servicios_no_esenciales"],
    "corrientes": ["hogar", "transporte", "salidas"],
    "irregulares": ["shopping", "otros"],
}

MAXIMUM_PERCENTAGES_PER_CATEGORY = {
    "alquileres": 30,
    "servicios_esenciales": 7,
    "servicios_no_esenciales": 5,
    "hogar": 15,
    "transporte": 5,
    "salidas": 8,
    "shopping": 7,
    "otros": 3,
}


def _calculate_month_totals(mes, df):
    fila_total = df.iloc[-1]
    fila_limpia = {
        cat: pd.to_numeric(
            fila_total[cat].replace("$", "").replace(",", "").strip(),
            errors="coerce",
        )
        for cat in EXPENSES_GROUPS["fijos"]
        + EXPENSES_GROUPS["corrientes"]
        + EXPENSES_GROUPS["irregulares"]
    }
    fila_limpia["mes"] = mes
    return fila_limpia


def get_expenses_dataframe() -> pd.DataFrame:
    months = get_months_until_now()
    month_urls = {
        month: f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={month}"
        for month in months
    }

    months_totals = []

    for mes in months:
        url = month_urls[mes]
        df = pd.read_csv(
            url,
            usecols=EXPENSES_GROUPS["fijos"]
            + EXPENSES_GROUPS["corrientes"]
            + EXPENSES_GROUPS["irregulares"],
        )
        months_totals.append(_calculate_month_totals(mes, df))
    return pd.DataFrame(months_totals).set_index("mes")


def get_next_month_expenses_dataframe() -> pd.DataFrame:
    next_month = get_next_month()
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={next_month}"
    if next_month == "enero":
        url = f"https://docs.google.com/spreadsheets/d/{NEXT_YEAR_EXPENSES_SPREADHSEET_ID}/gviz/tq?tqx=out:csv&sheet={next_month}"

    months_totals = []

    df = pd.read_csv(
        url,
        usecols=EXPENSES_GROUPS["fijos"]
        + EXPENSES_GROUPS["corrientes"]
        + EXPENSES_GROUPS["irregulares"],
    )
    months_totals.append(_calculate_month_totals(next_month, df))
    return pd.DataFrame(months_totals).set_index("mes")


def get_next_month_available_money_per_category():
    """Uses get_next_month_expenses_dataframe as well as get_last_net_salary to calculate available money per category for next month, based on the specified maximum percentages per categories"""
    next_month_expenses_df = get_next_month_expenses_dataframe()
    last_net_salary = get_last_net_salary()

    available_money_per_category = {}
    for category, max_percentage in MAXIMUM_PERCENTAGES_PER_CATEGORY.items():
        max_amount_for_category = (max_percentage / 100) * last_net_salary
        planned_expense = next_month_expenses_df.at[
            next_month_expenses_df.index[0], category
        ]
        available_money_per_category[category] = float(
            max_amount_for_category - planned_expense
        )

    return available_money_per_category


# available = get_next_month_available_money_per_category()

# for k, v in available.items():
#     print(f"Available money for {k} in next month: ${v:,.2f}")
