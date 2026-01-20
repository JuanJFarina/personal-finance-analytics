from typing import Any

from personal_finance_analytics.domain.months import get_remaining_days_in_current_month

from .it_salaries import (
    get_it_salary_percentile,
    get_it_salary_rank_per_seniority,
    get_junior_to_senior_delta,
    get_personal_salary_it_delta_adjusted,
)
from .entities import AvailableFunds, SalaryAnalytics
from .expenses import (
    get_category_funds_list,
    get_current_month_estimated_balance,
    get_current_month_expenses,
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
            it_delta_adjusted_salary=get_personal_salary_it_delta_adjusted(),
        )

    @staticmethod
    def month_expenses_analysis() -> AvailableFunds:
        current_month_expenses_df = get_current_month_expenses()
        current_month_estimated_balance = get_current_month_estimated_balance()
        current_month_salary = get_current_month_salary()
        current_balance = (current_month_salary * 0.7) - current_month_expenses_df.sum(
            axis=1
        ).iloc[0]

        available_funds: dict[str, Any] = {
            "net_salary": f"$ {current_month_salary:,.0f}"
        }

        category_funds_list = get_category_funds_list(
            current_month_expenses_df, current_month_salary
        )[0]

        available_funds["category_funds"] = category_funds_list

        available_funds["balance"] = f"$ {current_balance:,.0f}"
        available_funds["estimated_month_balance"] = (
            f"$ {(current_month_salary * 0.7) - current_month_estimated_balance:,.0f}"
        )
        available_funds["daily_limit"] = (
            f"Your daily limit for the rest of the month is $ {(current_balance / get_remaining_days_in_current_month()):,.0f}"
        )

        print(f"{available_funds = }")

        return AvailableFunds.model_validate(available_funds)
