from .exceptions import AuthorizationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request


async def authorization_exception_handler(_: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=401,
        content={"message": "Oops! Wrong password"},
    )
