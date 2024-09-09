import pytest
from fastapi.testclient import TestClient
from fastapi import Response
from sqlalchemy.orm import Session
from app.db.models import Profile
from tests.constants import PROFILES_TO_CREATE, PROFILES_TO_UPDATE, PROFILES_TO_DELETE, AFTER_DELETE_PROFILES, PROFILE_DATA, NON_VALID_PROFILE_ID
from tests.utils import assert_profile_match, assert_data_not_found, create_profiles


class TestProfileCRUD:
    @pytest.fixture(autouse=True)
    def setup(self, db_session: Session, test_client: TestClient):
        self.db = db_session
        self.client = test_client

    def test_create_profile(self):
        """
        Test the create profile endpoint
        """
        create_profiles(self.client, self.db, PROFILES_TO_CREATE)

    def test_get_profile(self):
        """
        Test the get profile endpoint
        """
        # Get the profile data
        for i in range(1, PROFILES_TO_UPDATE+1):
            response = self.client.get(f"/v1/profile/{i}/get")
            assert response.status_code == 200
            fetched_profile = response.json()
            assert_profile_match(fetched_profile, PROFILE_DATA)

        response = self.client.get(f"/v1/profile/{NON_VALID_PROFILE_ID}/get")
        assert_data_not_found(response, "profile-not-found")

    def test_update_profile(self):
        """
        Test the update profile endpoint
        """
        # Update the profile data
        updated_profile_data = PROFILE_DATA.copy()
        updated_profile_data["first_name"] = "Updated"
        updated_profile_data["last_name"] = "Name"

        # Call to update the profile data
        for i in range(1, PROFILES_TO_UPDATE+1):
            response = self.client.put(
                f"/v1/profile/{i}/update", json=updated_profile_data)
            assert response.status_code == 200
            updated_profile = response.json()
            assert_profile_match(updated_profile, updated_profile_data)

        # Validate the updated profiles
        for i in range(1, PROFILES_TO_UPDATE+1):
            response = self.client.get(f"/v1/profile/{i}/get")
            assert response.status_code == 200
            updated_profile = response.json()
            assert_profile_match(updated_profile, updated_profile_data)

        # Call to update the profile data that does not exist
        response = self.client.put(
            f"/v1/profile/{NON_VALID_PROFILE_ID}/update", json=updated_profile_data)
        assert_data_not_found(response, "profile-not-found")

    def test_delete_profile(self):
        """
        Test the delete profile endpoint
        """
        # Call to delete the profile data
        for i in range(75, 75 + PROFILES_TO_DELETE):
            response = self.client.delete(f"/v1/profile/{i}/delete")
            assert response.status_code == 200
            deleted_profile = response.json()
            assert_profile_match(deleted_profile, PROFILE_DATA)

        # Validate that the profile is deleted from the database
        for i in range(75, 75 + PROFILES_TO_DELETE):
            response = self.client.get(f"/v1/profile/{i}/get")
            assert_data_not_found(response, "profile-not-found")

        # Call to delete the profile data that does not exist
        response = self.client.delete(
            f"/v1/profile/{NON_VALID_PROFILE_ID}/delete")
        assert_data_not_found(response, "profile-not-found")

        # Validate the number of profiles
        total_profiles = self.db.query(Profile).count()
        assert total_profiles == PROFILES_TO_CREATE - PROFILES_TO_DELETE

    def call_get_all(self):
        """
        Call the get all profiles endpoint
        """
        # Get all profiles with default values
        response = self.client.get("/v1/profile/all")
        assert response.status_code == 200
        all_profiles = response.json()
        assert all_profiles["total"] == AFTER_DELETE_PROFILES
        assert len(all_profiles["profiles"]) == 10
        assert all_profiles["previous_url"] is None
        assert all_profiles["next_url"] is not None
        return all_profiles

    def test_get_all(self):
        """
        Test the get all profiles endpoint
        """
        self.call_get_all()

    def test_get_all_next_url(self):
        """
        Test the get all profiles endpoint with pagination checking the next url
        """
        all_profiles = self.call_get_all()
        assert all_profiles["next_url"] is not None

        # Get the next page
        response = self.client.get(all_profiles["next_url"])
        assert response.status_code == 200
        all_profiles = response.json()
        assert all_profiles["previous_url"] is not None
        assert all_profiles["next_url"] is not None
        assert all_profiles["total"] == AFTER_DELETE_PROFILES
        assert len(all_profiles["profiles"]) == 10

    def test_get_all_with_large_limit(self):
        """
        Test the get all profiles endpoint with a large limit
        """
        # Get large number of profiles
        response = self.client.get("/v1/profile/all?limit=100")
        assert response.status_code == 200
        all_profiles = response.json()
        assert all_profiles["total"] == AFTER_DELETE_PROFILES
        assert len(all_profiles["profiles"]) == AFTER_DELETE_PROFILES
        assert all_profiles["previous_url"] is None
        assert all_profiles["next_url"] is None

    def test_get_all_skip_more_than_total(self):
        """
        Test the get all profiles endpoint with skip more than total of profiles
        """
        # Get large number of profiles
        response = self.client.get("/v1/profile/all?skip=150")
        assert response.status_code == 200
        all_profiles = response.json()
        assert all_profiles["total"] == AFTER_DELETE_PROFILES
        assert len(all_profiles["profiles"]) == AFTER_DELETE_PROFILES % 10
        assert all_profiles["previous_url"] is not None
        assert all_profiles["next_url"] is None

    def test_get_all_with_filter(self):
        """
        Test the get all profiles endpoint with a filter for name and last name
        """
        # Get all profiles with name filter
        response = self.client.get(
            "/v1/profile/all?q=Updated&skip=10&limit=50")
        assert response.status_code == 200
        all_profiles = response.json()
        assert all_profiles["total"] == PROFILES_TO_UPDATE
        assert len(all_profiles["profiles"]) == 40
