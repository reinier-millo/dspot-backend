import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.constants import PROFILES_FRIENDSHIPS_TO_CREATE
from tests.utils import create_friendships


class TestGetFriends:
    @pytest.fixture(autouse=True)
    def setup(self, db_session: Session, test_client: TestClient):
        self.db = db_session
        self.client = test_client

    def test_get_friends(self):
        """
        Test the get friends endpoint
        """
        # Call to create the friendships
        create_friendships(self.client, self.db,
                           PROFILES_FRIENDSHIPS_TO_CREATE)

        # Check the friends for each profile
        for i in range(1, PROFILES_FRIENDSHIPS_TO_CREATE):
            response = self.client.get(
                f"/v1/profile/{i}/friends?limit={PROFILES_FRIENDSHIPS_TO_CREATE}")
            assert response.status_code == 200
            friends = response.json()
            assert friends["total"] == PROFILES_FRIENDSHIPS_TO_CREATE - 1
            assert len(friends["profiles"]
                       ) == PROFILES_FRIENDSHIPS_TO_CREATE - 1
            assert friends["next_url"] is None
            assert friends["previous_url"] is None

    def test_get_friends_next_url(self):
        """
        Test the get friends endpoint with pagination checking the next url
        """
        response = self.client.get("/v1/profile/1/friends?skip=0&limit=3")
        assert response.status_code == 200
        all_friends = response.json()
        assert all_friends["next_url"] is not None
        assert all_friends["previous_url"] is None
        assert len(all_friends["profiles"]) == 3

        # Get the next page
        response = self.client.get(all_friends["next_url"])
        assert response.status_code == 200
        all_friends = response.json()
        assert all_friends["previous_url"] is not None
        assert all_friends["next_url"] is not None
        assert all_friends["total"] == PROFILES_FRIENDSHIPS_TO_CREATE - 1
        assert len(all_friends["profiles"]) == 3

    def test_get_friends_with_large_limit(self):
        """
        Test the get friends endpoint with a large limit
        """
        # Get large number of friends
        response = self.client.get("/v1/profile/1/friends?limit=100")
        assert response.status_code == 200
        all_friends = response.json()
        assert all_friends["total"] == PROFILES_FRIENDSHIPS_TO_CREATE - 1
        assert len(all_friends["profiles"]
                   ) == PROFILES_FRIENDSHIPS_TO_CREATE - 1
        assert all_friends["previous_url"] is None
        assert all_friends["next_url"] is None

    def test_get_friends_skip_more_than_total(self):
        """
        Test the get friends endpoint with skip more than total of friends
        """
        # Get large number of friends
        response = self.client.get("/v1/profile/1/friends?skip=150&limit=5")
        assert response.status_code == 200
        all_friends = response.json()
        assert all_friends["total"] == PROFILES_FRIENDSHIPS_TO_CREATE - 1
        assert len(all_friends["profiles"]) == (
            PROFILES_FRIENDSHIPS_TO_CREATE - 1) % 5
        assert all_friends["previous_url"] is not None
        assert all_friends["next_url"] is None
