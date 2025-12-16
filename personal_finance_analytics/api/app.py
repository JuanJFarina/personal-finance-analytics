from fastapi import FastAPI
from personal_finance_analytics import __version__
from .error_handling import AuthorizationError, authorization_exception_handler
from .routes import available_funds_router

app = FastAPI(
    title="Personal Finance Analytics API",
    description="API for Personal Finance Analytics application",
    version=__version__,
)

app.add_exception_handler(AuthorizationError, authorization_exception_handler)  # type: ignore
app.include_router(available_funds_router)
