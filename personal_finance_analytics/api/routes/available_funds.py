import os
from fastapi import APIRouter
from pydantic import BaseModel

from personal_finance_analytics.api.error_handling import AuthorizationError
from personal_finance_analytics.domain.entities import AvailableFunds
from personal_finance_analytics.domain.expenses import (
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
    return get_current_month_available_money_per_category()
