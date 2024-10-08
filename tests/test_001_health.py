"""
Tests for the health endpoint
"""
import pytest
from fastapi.testclient import TestClient
from app.constants import API_VERSION


class TestHealth:
    """
    Tests for the health endpoint
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_client: TestClient):
        """
        Setup the test
        """
        self.client = test_client  # pylint: disable=attribute-defined-outside-init

    def test_health(self):
        """
        Test the health endpoint
        """
        response_root = self.client.get("/")
        response_health = self.client.get("/health")

        assert response_root.status_code == 200
        assert response_health.status_code == 200

        health_data = response_health.json()

        assert health_data["status"] == "ok"
        assert health_data["version"] == API_VERSION
        assert health_data == response_root.json()
