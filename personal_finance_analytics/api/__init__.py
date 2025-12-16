import uvicorn


def run_backend() -> None:
    uvicorn.run(
        "personal_finance_analytics.api.app:app",
        host="127.0.0.1",
        port=8000,
        loop="asyncio",
        reload=True,
    )
