from typing import Any

from .it_salaries import (
    get_it_salary_percentile,
    get_it_salary_rank_per_seniority,
    get_junior_to_senior_delta,
)
from .entities import AvailableFunds, SalaryAnalytics
from .expenses import (
    get_current_month_estimated_balance,
    get_current_month_expenses,
    MAXIMUM_PERCENTAGES_PER_CATEGORY,
)
from .salaries import (
    get_last_adjusted_salary,
    get_current_month_salary,
    get_personal_delta,
    get_salary_variance,
)


class FinanceAnalyst:
    @staticmethod
    def salary_analysis() -> SalaryAnalytics:
        return SalaryAnalytics(
            net_salary=f"$ {get_current_month_salary():,.2f}",
            adjusted_salary=f"$ {get_last_adjusted_salary():,.2f}",
            salary_variance_in_usd=get_salary_variance(),
            it_salary_percentile=f"{get_it_salary_percentile():.2f} %",
            rank_per_seniority=get_it_salary_rank_per_seniority()[0],
            junior_to_senior_delta=get_junior_to_senior_delta(),
            personal_delta=get_personal_delta(),
        )

    @staticmethod
    def month_expenses_analysis() -> AvailableFunds:
        current_month_expenses_df = get_current_month_expenses()
        current_month_estimated_balance = get_current_month_estimated_balance()
        current_month_salary = get_current_month_salary()

        available_funds: dict[str, Any] = {
            "net_salary": f"$ {current_month_salary:,.0f}"
        }

        category_funds_list = list[dict[str, str]]()
        for category, max_percentage in MAXIMUM_PERCENTAGES_PER_CATEGORY.items():
            max_amount_for_category = (max_percentage / 100) * current_month_salary
            planned_expense = current_month_expenses_df.at[
                current_month_expenses_df.index[0], category
            ]
            category_funds_list.append(
                {
                    "category": category,
                    "max_allocation": f"$ {max_amount_for_category:,.0f}",
                    "available_funds": f"$ {float(max_amount_for_category - float(planned_expense)):,.0f}",
                }
            )

        available_funds["category_funds"] = category_funds_list

        available_funds["balance"] = (
            f"$ {(current_month_salary * 0.7) - current_month_expenses_df.sum(axis=1).iloc[0]:,.0f}"
        )
        available_funds["estimated_month_balance"] = (
            f"$ {(current_month_salary * 0.7) - current_month_estimated_balance:,.0f}"
        )

        return AvailableFunds.model_validate(available_funds)
