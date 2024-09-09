import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models import friendship as FriendshipTable
from app.models.errors import PROFILE_NOT_FOUND, FRIEND_NOT_FOUND, FRIENDSHIP_NOT_FOUND, FRIENDSHIP_SAME_PROFILE
from tests.constants import PROFILES_FRIENDSHIPS_TO_CREATE, NON_VALID_PROFILE_ID
from tests.utils import assert_data_not_found, create_friendships


class TestFriendshipCRUD:
    @pytest.fixture(autouse=True)
    def setup(self, db_session: Session, test_client: TestClient):
        self.db = db_session
        self.client = test_client

    def test_create_friendship(self):
        """
        Test the create friendship endpoint
        """
        # Call to create the friendships
        create_friendships(self.client, self.db,
                           PROFILES_FRIENDSHIPS_TO_CREATE)

    def test_try_create_existing_friendship(self):
        """
        Test the create friendship endpoint with existing friendship data
        """
        response = self.client.post(
            "/v1/friendship/create", json={"profile_id": 1, "friend_id": 2})
        assert response.status_code == 201
        assert response.json() == {"profile_id": 1, "friend_id": 2}

    def test_try_create_friendship_same_profile(self):
        """
        Test the create friendship endpoint with existing friendship data
        """
        response = self.client.post(
            "/v1/friendship/create", json={"profile_id": 1, "friend_id": 1})
        assert response.status_code == 400
        assert response.json() == {"detail": FRIENDSHIP_SAME_PROFILE}

    def test_create_friendship_with_invalid_profile_id(self):
        """
        Test the create friendship endpoint with invalid profile id
        """
        response = self.client.post(
            "/v1/friendship/create", json={"profile_id": NON_VALID_PROFILE_ID, "friend_id": 1})
        assert_data_not_found(response, PROFILE_NOT_FOUND)

    def test_create_friendship_with_invalid_friend_id(self):
        """
        Test the create friendship endpoint with invalid friend id
        """
        response = self.client.post(
            "/v1/friendship/create", json={"profile_id": 1, "friend_id": NON_VALID_PROFILE_ID})
        assert_data_not_found(response, FRIEND_NOT_FOUND)

    def test_check_friendship_count(self):
        """
        Check the number of friendships
        """
        friendship_count = self.db.query(
            func.count()).select_from(FriendshipTable).scalar()
        assert friendship_count == PROFILES_FRIENDSHIPS_TO_CREATE * \
            (PROFILES_FRIENDSHIPS_TO_CREATE - 1) / 2

    def test_delete_friendship(self):
        """
        Test the delete friendship endpoint
        """
        # Call to create the friendships
        for i in range(1, PROFILES_FRIENDSHIPS_TO_CREATE):
            for j in range(i+1, PROFILES_FRIENDSHIPS_TO_CREATE+1):
                response = self.client.delete(f"/v1/friendship/{i}/{j}/delete")
                assert response.status_code == 200
                friendship = response.json()
                assert friendship == {"profile_id": i, "friend_id": j}

        # Call to delete the friendships that doesn't exist
        response = self.client.delete("/v1/friendship/1/2/delete")
        assert_data_not_found(response, FRIENDSHIP_NOT_FOUND)

    def test_check_friendship_count_after_delete(self):
        """
        Check the number of friendships after delete
        """
        friendship_count = self.db.query(
            func.count()).select_from(FriendshipTable).scalar()
        assert friendship_count == 0
