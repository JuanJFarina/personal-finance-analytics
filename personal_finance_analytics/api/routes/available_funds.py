import os
from fastapi import APIRouter
from pydantic import BaseModel

from personal_finance_analytics.api.error_handling import AuthorizationError

router = APIRouter()


class AuthorizedRequest(BaseModel):
    password: str

    def validate_password(self) -> None:
        expected_password = os.getenv("API_PASSWORD")
        if self.password != expected_password:
            raise AuthorizationError("Unauthorized")


@router.post("/available-funds")
async def get_available_funds(request: AuthorizedRequest):
    request.validate_password()
    return {"available_funds": 1000}  # TODO: Placeholder implementation
