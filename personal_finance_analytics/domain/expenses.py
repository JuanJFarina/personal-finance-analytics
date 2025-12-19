import os
import pandas as pd

from typing import Any

from .entities import AvailableFunds

from .months import get_months_until_now, get_current_month, get_next_month
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


def get_expenses_dataframe() -> pd.DataFrame:
    months = get_months_until_now()
    month_urls = {
        month: f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={month}"
        for month in months
    }

    months_totals = []

    for month in months:
        url = month_urls[month]
        _read_csv_and_calculate_totals(month, url, months_totals)
    return pd.DataFrame(months_totals).set_index("mes")


def get_current_month_expenses_dataframe() -> pd.DataFrame:
    current_month = get_current_month()
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={current_month}"

    months_totals = []

    _read_csv_and_calculate_totals(current_month, url, months_totals)
    return pd.DataFrame(months_totals).set_index("mes")


def get_next_month_expenses_dataframe() -> pd.DataFrame:
    next_month = get_next_month()
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={next_month}"
    if next_month == "enero":
        url = f"https://docs.google.com/spreadsheets/d/{NEXT_YEAR_EXPENSES_SPREADHSEET_ID}/gviz/tq?tqx=out:csv&sheet={next_month}"

    months_totals = []

    _read_csv_and_calculate_totals(next_month, url, months_totals)
    return pd.DataFrame(months_totals).set_index("mes")


def get_next_month_available_money_per_category() -> dict[str, dict[str, str]]:
    next_month_expenses_df = get_next_month_expenses_dataframe()
    print(f"Next month expenses: {next_month_expenses_df}")
    last_net_salary = get_last_net_salary()
    print(f"Last net salary: {last_net_salary}")

    available_money_per_category = {}
    for category, max_percentage in MAXIMUM_PERCENTAGES_PER_CATEGORY.items():
        max_amount_for_category = (max_percentage / 100) * last_net_salary
        planned_expense = next_month_expenses_df.at[
            next_month_expenses_df.index[0], category
        ]
        available_money_per_category[category] = {
            f"Maximum: {max_amount_for_category:,.2f}": f"Available: {float(max_amount_for_category - planned_expense):,.2f}"
        }

    print(
        f"Available money per category for next month: {available_money_per_category}"
    )

    return available_money_per_category


def get_current_month_available_money_per_category() -> AvailableFunds:
    current_month_expenses_df = get_current_month_expenses_dataframe()
    print(f"Current month expenses: \n{current_month_expenses_df}")
    last_net_salary = f"{get_last_net_salary():,.2f}"
    print(f"Last net salary: {last_net_salary}")

    available_funds: dict[str, Any] = {"net_salary": last_net_salary}

    category_funds_list = list[dict[str, str]]()
    for category, max_percentage in MAXIMUM_PERCENTAGES_PER_CATEGORY.items():
        max_amount_for_category = (max_percentage / 100) * last_net_salary
        planned_expense = current_month_expenses_df.at[
            current_month_expenses_df.index[0], category
        ]
        category_funds_list.append(
            {
                "category": category,
                "max_allocation": f"{max_amount_for_category:,.2f}",
                "available_funds": f"{float(max_amount_for_category - float(planned_expense)):,.2f}",
            }
        )

    available_funds["category_funds"] = category_funds_list

    available_funds["balance"] = (
        f"{(last_net_salary * 0.7) - current_month_expenses_df.sum(axis=1).iloc[0]:,.2f}"
    )

    return AvailableFunds.model_validate(available_funds)


def _calculate_month_totals(mes: str, df: pd.DataFrame) -> dict[str, str | float]:
    fila_total = df.iloc[-1]
    fila_limpia: dict[str, str | float] = {
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


def _read_csv_and_calculate_totals(
    next_month: str, url: str, months_totals: list[dict[str, str | float]]
) -> None:
    df = pd.read_csv(
        url,
        usecols=EXPENSES_GROUPS["fijos"]
        + EXPENSES_GROUPS["corrientes"]
        + EXPENSES_GROUPS["irregulares"],
    )
    months_totals.append(_calculate_month_totals(next_month, df))
