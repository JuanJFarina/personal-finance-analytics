from personal_finance_analytics.domain import get_category_funds_list
import pandas as pd


def test_get_category_funds_list(
    current_month_expenses_df: pd.DataFrame, current_month_salary: float
) -> None:
    get_category_funds_list(current_month_expenses_df, current_month_salary)
