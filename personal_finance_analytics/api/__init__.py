import uvicorn

from .app import app
from personal_finance_analytics.utils import Settings


__all__ = ["app"]


def run_backend() -> None:
    uvicorn.run(
        "personal_finance_analytics.api.app:app",
        host=Settings.HOST,
        port=8000,
        loop="asyncio",
        reload=True,
    )
