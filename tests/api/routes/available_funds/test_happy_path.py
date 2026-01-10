from fastapi.testclient import TestClient
from personal_finance_analytics.domain import AvailableFunds


def test_get_available_funds(api_client: TestClient, test_password: str) -> None:
    response = api_client.get(f"/available-funds/{test_password}")
    assert AvailableFunds.model_validate(response.json())
