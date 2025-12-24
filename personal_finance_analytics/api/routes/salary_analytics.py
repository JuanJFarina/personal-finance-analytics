import logging
from fastapi import APIRouter

from personal_finance_analytics.api import SalaryAnalyticsException
from .dependencies import AuthDepends

router = APIRouter()


@router.get("/salary-analytics/{password}")
async def get_salary_analytics(
    password: AuthDepends,
) -> dict[str, str]:
    try:
        return {}
    except Exception as e:
        logging.error(f"Error getting salary analytics: {e}")
        raise SalaryAnalyticsException
