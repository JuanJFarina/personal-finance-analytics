import logging
from fastapi import APIRouter

from personal_finance_analytics.api import AvailableFundsException
from .dependencies import AuthDepends
from personal_finance_analytics.domain import (
    AvailableFunds,
    get_current_month_available_money_per_category,
)

router = APIRouter()


@router.get("/available-funds/{password}")
async def get_available_funds(
    password: AuthDepends,
) -> AvailableFunds:
    try:
        return get_current_month_available_money_per_category()
    except Exception as e:
        logging.error(f"Error getting available funds: {e}")
        raise AvailableFundsException
