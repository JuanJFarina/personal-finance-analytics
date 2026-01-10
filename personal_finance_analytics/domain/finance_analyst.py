import logging
from typing import Any
from .entities import AvailableFunds
from .expenses import (
    get_current_month_estimated_balance,
    get_current_month_expenses,
    MAXIMUM_PERCENTAGES_PER_CATEGORY,
)
from .salaries import get_last_adjusted_salary, get_current_month_salary


class FinanceAnalyst:
    @staticmethod
    def salary_analysis() -> dict[str, str]:
        return {
            "net_salary": f"{get_current_month_salary():,.2f}",
            "adjusted_salary": f"{get_last_adjusted_salary():,.2f}",
        }

    @staticmethod
    def month_expenses_analysis() -> AvailableFunds:
        current_month_expenses_df = get_current_month_expenses()
        current_month_estimated_balance = get_current_month_estimated_balance()
        logging.info(f"Current month expenses: \n{current_month_expenses_df}")
        current_month_salary = get_current_month_salary()
        logging.info(f"Last net salary: {current_month_salary}")

        available_funds: dict[str, Any] = {"net_salary": f"${current_month_salary:,.0f}"}

        category_funds_list = list[dict[str, str]]()
        for category, max_percentage in MAXIMUM_PERCENTAGES_PER_CATEGORY.items():
            max_amount_for_category = (max_percentage / 100) * current_month_salary
            planned_expense = current_month_expenses_df.at[
                current_month_expenses_df.index[0], category
            ]
            category_funds_list.append(
                {
                    "category": category,
                    "max_allocation": f"${max_amount_for_category:,.0f}",
                    "available_funds": f"${float(max_amount_for_category - float(planned_expense)):,.0f}",
                }
            )

        available_funds["category_funds"] = category_funds_list

        available_funds["balance"] = (
            f"${(current_month_salary * 0.7) - current_month_expenses_df.sum(axis=1).iloc[0]:,.0f}"
        )
        available_funds["estimated_month_balance"] = (
            f"${(current_month_salary * 0.7) - current_month_estimated_balance:,.0f}"
        )

        return AvailableFunds.model_validate(available_funds)
