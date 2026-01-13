import logging
from fastapi import APIRouter

from personal_finance_analytics.utils import SalaryAnalyticsException
from personal_finance_analytics.domain import FinanceAnalyst, SalaryAnalytics
from .dependencies import AuthDepends

router = APIRouter()


@router.get("/salary-analytics/{password}")
async def get_salary_analytics(
    password: AuthDepends,
) -> SalaryAnalytics:
    try:
        return FinanceAnalyst.salary_analysis()
    except Exception as e:
        logging.error(f"Error getting salary analytics: {e}")
        raise SalaryAnalyticsException
