import logging
import os
from fastapi import APIRouter
from pydantic import BaseModel

from personal_finance_analytics.api.error_handling import (
    AuthorizationError,
    AvailableFundsException,
)
from personal_finance_analytics.domain import (
    AvailableFunds,
    get_current_month_available_money_per_category,
)

router = APIRouter()


class AuthorizedRequest(BaseModel):
    password: str

    def validate_password(self) -> None:
        expected_password = os.getenv("API_PASSWORD")
        if self.password != expected_password:
            raise AuthorizationError("Unauthorized")


@router.post("/available-funds")
async def get_available_funds(request: AuthorizedRequest) -> AvailableFunds:
    request.validate_password()
    try:
        return get_current_month_available_money_per_category()
    except Exception as e:
        logging.error(f"Error getting available funds: {e}")
        raise AvailableFundsException


@router.get("/available-funds/{password}")
async def get_available_funds_by_password(
    password: str,
) -> AvailableFunds:
    request = AuthorizedRequest(password=password)
    request.validate_password()
    try:
        return get_current_month_available_money_per_category()
    except Exception as e:
        logging.error(f"Error getting available funds: {e}")
        raise AvailableFundsException
