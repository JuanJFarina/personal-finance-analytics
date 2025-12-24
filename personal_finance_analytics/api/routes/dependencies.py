import os
from typing import Annotated
from fastapi import Depends

from personal_finance_analytics.api.error_handling import AuthorizationError


async def authorize_request(password: str):
    expected_password = os.getenv("API_PASSWORD")
    if password != expected_password:
        raise AuthorizationError("Unauthorized")


AuthDepends = Annotated[str, Depends(authorize_request)]
