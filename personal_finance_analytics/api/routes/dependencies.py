from typing import Annotated
from fastapi import Depends

from personal_finance_analytics.utils import AuthorizationError, Settings


async def authorize_request(password: str):
    expected_password = Settings.API_PASSWORD
    if password != expected_password:
        raise AuthorizationError("Unauthorized")


AuthDepends = Annotated[str, Depends(authorize_request)]
