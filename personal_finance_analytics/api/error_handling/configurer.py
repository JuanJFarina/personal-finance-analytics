from fastapi import FastAPI
from personal_finance_analytics.utils import (
    ExpensesSpreadsheetException,
    SalariesSpreadsheetException,
    AuthorizationError,
    AvailableFundsException,
    SalaryAnalyticsException,
)
from .handlers import (
    authorization_exception_handler,
    available_funds_exception_handler,
    expenses_exception_handler,
    salaries_exception_handler,
    salary_analytics_exception_handler,
)


def configure_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AuthorizationError, authorization_exception_handler)  # type: ignore
    app.add_exception_handler(
        AvailableFundsException, available_funds_exception_handler
    )
    app.add_exception_handler(ExpensesSpreadsheetException, expenses_exception_handler)  # type: ignore
    app.add_exception_handler(SalariesSpreadsheetException, salaries_exception_handler)  # type: ignore
    app.add_exception_handler(
        SalaryAnalyticsException, salary_analytics_exception_handler
    )
