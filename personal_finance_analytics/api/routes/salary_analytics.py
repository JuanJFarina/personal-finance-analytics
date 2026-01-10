import logging
from fastapi import APIRouter

from personal_finance_analytics.api.error_handling import SalaryAnalyticsException
from personal_finance_analytics.domain import FinanceAnalyst
from .dependencies import AuthDepends

router = APIRouter()


@router.get("/salary-analytics/{password}")
async def get_salary_analytics(
    password: AuthDepends,
) -> dict[str, str]:
    try:
        return FinanceAnalyst.salary_analysis()
    except Exception as e:
        logging.error(f"Error getting salary analytics: {e}")
        raise SalaryAnalyticsException
