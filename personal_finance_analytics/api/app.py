from fastapi import FastAPI
from personal_finance_analytics import __version__
from personal_finance_analytics.domain.exceptions import (
    ExpensesSpreadsheetException,
    SalariesSpreadsheetException,
)
from .error_handling import (
    AuthorizationError,
    AvailableFundsException,
    authorization_exception_handler,
    available_funds_exception_handler,
    expenses_exception_handler,
    salaries_exception_handler,
)
from .routes import available_funds_router

app = FastAPI(
    title="Personal Finance Analytics API",
    description="API for Personal Finance Analytics application",
    version=__version__,
)

app.add_exception_handler(AuthorizationError, authorization_exception_handler)  # type: ignore
app.add_exception_handler(AvailableFundsException, available_funds_exception_handler)  # type: ignore
app.add_exception_handler(ExpensesSpreadsheetException, expenses_exception_handler)  # type: ignore
app.add_exception_handler(SalariesSpreadsheetException, salaries_exception_handler)  # type: ignore
app.include_router(available_funds_router)
