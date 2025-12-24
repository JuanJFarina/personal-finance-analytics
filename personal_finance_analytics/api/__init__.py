import uvicorn
import os

from .error_handling import (
    AuthorizationError,
    AvailableFundsException,
    SalaryAnalyticsException,
)

__all__ = ["AuthorizationError", "AvailableFundsException", "SalaryAnalyticsException"]


def run_backend() -> None:
    uvicorn.run(
        "personal_finance_analytics.api.app:app",
        host=os.getenv("HOST") or "0.0.0.0",
        port=8000,
        loop="asyncio",
        reload=True,
    )
