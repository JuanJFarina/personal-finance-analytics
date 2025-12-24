from personal_finance_analytics.domain.exceptions import (
    ExpensesSpreadsheetException,
    SalariesSpreadsheetException,
)
from .exceptions import AuthorizationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request


async def authorization_exception_handler(_: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=401,
        content={"message": "Oops! Wrong password"},
    )


async def expenses_exception_handler(_: Request, exc: ExpensesSpreadsheetException):
    return JSONResponse(
        status_code=500,
        content={"message": "Error reading expenses spreadsheet."},
    )


async def salaries_exception_handler(_: Request, exc: SalariesSpreadsheetException):
    return JSONResponse(
        status_code=500,
        content={"message": "Error reading salaries spreadsheet."},
    )


async def available_funds_exception_handler(_: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=500,
        content={"message": "Error calculating available funds."},
    )


async def salary_analytics_exception_handler(_: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=500,
        content={"message": "Error calculating salary analytics."},
    )
