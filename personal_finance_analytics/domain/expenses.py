import logging
import pandas as pd

from personal_finance_analytics.infrastructure.expenses_data import get_expenses_data

from personal_finance_analytics.utils import Settings

from .months import get_months_until_now, get_current_month, get_next_month
from .salaries import get_current_month_salary

SPREADSHEET_ID = Settings.EXPENSES_SPREADSHEET_ID
NEXT_YEAR_EXPENSES_SPREADSHEET_ID = Settings.NEXT_YEAR_EXPENSES_SPREADSHEET_ID


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


EXPENSES_GROUPS = {
    "fijos": ["alquileres", "servicios_esenciales", "servicios_no_esenciales"],
    "corrientes": ["hogar", "transporte", "salidas"],
    "irregulares": ["shopping", "otros"],
}


def _get_month_expenses_totals(
    month: str, url: str, months_totals: list[dict[str, str | float]]
) -> None:
    df = get_expenses_data(
        url,
        cols=EXPENSES_GROUPS["fijos"]
        + EXPENSES_GROUPS["corrientes"]
        + EXPENSES_GROUPS["irregulares"],
    )
    months_totals.append(_calculate_month_expenses_totals(month, df))


def _get_month_estimated_expenses_sum(url: str) -> float:
    df = get_expenses_data(url, cols=["media movil"])
    return float(
        pd.to_numeric(
            df.iloc[-1]["media movil"].replace("$", "").replace(",", "").strip(),
            errors="coerce",
        )
    )


def _calculate_month_expenses_totals(
    mes: str, df: pd.DataFrame
) -> dict[str, str | float]:
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


def get_ongoing_year_expenses() -> pd.DataFrame:
    months = get_months_until_now()
    month_urls = {
        month: f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={month}"
        for month in months
    }

    months_totals = []

    for month in months:
        url = month_urls[month]
        _get_month_expenses_totals(month, url, months_totals)
    return pd.DataFrame(months_totals).set_index("mes")


def get_current_month_expenses() -> pd.DataFrame:
    current_month = get_current_month()
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={current_month}"

    months_totals = list[dict[str, str | float]]()

    _get_month_expenses_totals(current_month, url, months_totals)
    return pd.DataFrame(months_totals).set_index("mes")


def get_current_month_estimated_balance() -> float:
    current_month = get_current_month()
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={current_month}"
    return _get_month_estimated_expenses_sum(url)


def get_next_month_expenses() -> pd.DataFrame:
    next_month = get_next_month()
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={next_month}"
    if next_month == "enero":
        url = f"https://docs.google.com/spreadsheets/d/{NEXT_YEAR_EXPENSES_SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={next_month}"

    months_totals = []

    _get_month_expenses_totals(next_month, url, months_totals)
    return pd.DataFrame(months_totals).set_index("mes")


def get_next_month_available_money_per_category() -> dict[str, dict[str, str]]:
    next_month_expenses_df = get_next_month_expenses()
    logging.info(f"Next month expenses: {next_month_expenses_df}")
    last_net_salary = get_current_month_salary()
    logging.info(f"Last net salary: {last_net_salary}")

    available_money_per_category = {}
    for category, max_percentage in MAXIMUM_PERCENTAGES_PER_CATEGORY.items():
        max_amount_for_category = (max_percentage / 100) * last_net_salary
        planned_expense = next_month_expenses_df.at[
            next_month_expenses_df.index[0], category
        ]
        available_money_per_category[category] = {
            f"Maximum: {max_amount_for_category:,.2f}": f"Available: {float(max_amount_for_category - planned_expense):,.2f}"
        }

    logging.info(
        f"Available money per category for next month: {available_money_per_category}"
    )

    return available_money_per_category


def get_category_funds_list(
    current_month_expenses_df: pd.DataFrame, current_month_salary: float
) -> tuple[list[dict[str, str]], list[dict[str, str | float]]]:
    category_funds_list = list[dict[str, str]]()
    raw_category_funds_list = list[dict[str, str | float]]()
    for category, max_percentage in MAXIMUM_PERCENTAGES_PER_CATEGORY.items():
        max_amount_for_category = current_month_salary * max_percentage * 0.01
        current_money_spent = current_month_expenses_df.at[
            current_month_expenses_df.index[0], category
        ]
        category_funds_list.append(
            {
                "category": category,
                "max_allocation": f"$ {max_amount_for_category:,.0f}",
                "available_funds": f"$ {float(max_amount_for_category - float(current_money_spent)):,.0f}",
            }
        )
        raw_category_funds_list.append(
            {
                "category": category,
                "max_allocation": max_amount_for_category,
                "available_funds": max_amount_for_category - float(current_money_spent),
            }
        )

    return (category_funds_list, raw_category_funds_list)
