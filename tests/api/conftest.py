from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from personal_finance_analytics.api.app import app
from personal_finance_analytics.utils import Settings


@pytest.fixture
def api_client() -> TestClient:
    client = TestClient(app)
    return client


@pytest.fixture()
def test_password() -> Generator[str, None, None]:
    old_password = Settings.API_PASSWORD
    Settings.API_PASSWORD = "test_password"
    yield "test_password"
    Settings.API_PASSWORD = old_password
