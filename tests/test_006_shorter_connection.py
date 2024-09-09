import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.controllers.friendship import Friendship
from tests.constants import PROFILES_FRIENDSHIPS_TO_CREATE
from tests.utils import create_profiles, create_friendship


class TestShorterConnection:
    @pytest.fixture(autouse=True)
    def setup(self, db_session: Session, test_client: TestClient):
        self.db = db_session
        self.client = test_client

    def test_prepare_data(self):
        """
        Test to prepare the data to test the shorter connection
        """
        # Call to create the profiles
        create_profiles(self.client, self.db,
                        PROFILES_FRIENDSHIPS_TO_CREATE)

        # Call to create the friendships
        create_friendship(self.client, self.db, 3, 6)
        create_friendship(self.client, self.db, 3, 1)
        create_friendship(self.client, self.db, 1, 2)
        create_friendship(self.client, self.db, 2, 4)
        create_friendship(self.client, self.db, 6, 4)

    def test_get_all_friends(self):
        """
        Test the function to get all friends ids
        """
        friends = Friendship.get_all_friends(self.db, 3)
        assert friends == [1, 6]

    @pytest.mark.asyncio
    async def test_get_shorter_connection(self):
        """
        Test the get shorter connection function
        """
        path = await Friendship.get_connection(self.db, 3, 4)
        assert path == [3, 6, 4]

        path = await Friendship.get_connection(self.db, 6, 1)
        assert path == [6, 3, 1]

        path = await Friendship.get_connection(self.db, 1, 5)
        assert path == []

        path = await Friendship.get_connection(self.db, 4, 2)
        assert path == [4, 2]

    def test_get_shorter_connection_api(self):
        """
        Test the get shorter connection endpoint
        """
        response = self.client.get("/v1/friendship/3/4/connection")
        assert response.status_code == 200
        assert response.json() == {"path": [3, 6, 4]}

        response = self.client.get("/v1/friendship/6/1/connection")
        assert response.status_code == 200
        assert response.json() == {"path": [6, 3, 1]}

        response = self.client.get("/v1/friendship/1/5/connection")
        assert response.status_code == 200
        assert response.json() == {"path": []}

        response = self.client.get("/v1/friendship/4/2/connection")
        assert response.status_code == 200
        assert response.json() == {"path": [4, 2]}
