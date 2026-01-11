from fastapi.testclient import TestClient


def test_healthcheck(api_client: TestClient) -> None:
    response = api_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
