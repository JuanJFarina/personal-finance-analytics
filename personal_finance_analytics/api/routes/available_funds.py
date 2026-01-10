import logging
from fastapi import APIRouter

from personal_finance_analytics.api.error_handling import AvailableFundsException
from .dependencies import AuthDepends
from personal_finance_analytics.domain import AvailableFunds, FinanceAnalyst

router = APIRouter()


@router.get("/available-funds/{password}")
async def get_available_funds(
    password: AuthDepends,
) -> AvailableFunds:
    try:
        return FinanceAnalyst.month_expenses_analysis()
    except Exception as e:
        logging.error(f"Error getting available funds: {e}")
        raise AvailableFundsException
