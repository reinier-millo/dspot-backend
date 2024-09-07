from fastapi.testclient import TestClient
from app.constants import API_VERSION


def test_health(test_client: TestClient):
    """
    Test the health endpoint
    """
    response_root = test_client.get("/")
    response_health = test_client.get("/health")

    assert response_root.status_code == 200
    assert response_health.status_code == 200

    health_data = response_health.json()

    assert health_data["status"] == "ok"
    assert health_data["version"] == API_VERSION
    assert health_data == response_root.json()
