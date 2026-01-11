from fastapi import FastAPI
from personal_finance_analytics import __version__
from .error_handling import configure_exception_handlers
from .routes import available_funds_router, healthcheck_router, salary_analytics_router

app = FastAPI(
    title="Personal Finance Analytics API",
    description="API for Personal Finance Analytics application",
    version=__version__,
)

configure_exception_handlers(app)
app.include_router(available_funds_router)
app.include_router(healthcheck_router)
app.include_router(salary_analytics_router)
