import uvicorn
import os


def run_backend() -> None:
    uvicorn.run(
        "personal_finance_analytics.api.app:app",
        host=os.getenv("HOST") or "0.0.0.0",
        port=8000,
        loop="asyncio",
        reload=True,
    )
