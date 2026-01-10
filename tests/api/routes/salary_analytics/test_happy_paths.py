from fastapi.testclient import TestClient
from personal_finance_analytics.domain import SalaryAnalytics


def test_get_salary_analytics(api_client: TestClient, test_password: str) -> None:
    response = api_client.get(f"/salary-analytics/{test_password}")
    assert SalaryAnalytics.model_validate(response.json())
