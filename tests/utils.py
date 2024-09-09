"""
Utils for the tests
"""
from fastapi.testclient import TestClient
from fastapi import Response
from sqlalchemy.orm import Session
from app.db.models import Profile
from tests.constants import PROFILE_DATA


def assert_profile_match(created_profile: dict, expected_data: dict):
    """
    Helper function to assert that all keys in expected_data are present in created_profile
    and have matching values.
    """
    for key, value in expected_data.items():
        assert key in created_profile, f"Key '{key}' not found in created profile"
        assert created_profile[
            key] == value, f"Value mismatch for key '{key}': expected {value}, got {created_profile[key]}"


def assert_data_not_found(response: Response, expected_error_code: str):
    """
    Helper function to assert that the response status code is 404
    """
    assert response.status_code == 404
    assert response.json() == {"detail": expected_error_code}


def create_profiles(client: TestClient, db: Session, num_profiles: int):
    """
    Helper function to create a number of profiles
    """
    for _ in range(1, num_profiles+1):
        response = client.post(
            "/v1/profile/create", json=PROFILE_DATA)
        assert response.status_code == 201
        created_profile = response.json()
        assert_profile_match(created_profile, PROFILE_DATA)

    # Validate the number of profiles
    assert db.query(Profile).count() == num_profiles


def create_friendship(client: TestClient, profile_id: int, friend_id: int):
    """
    Helper function to create a friendship
    """
    response = client.post(
        "/v1/friendship/create", json={"profile_id": profile_id, "friend_id": friend_id})
    assert response.status_code == 201
    friendship = response.json()
    assert friendship == {"profile_id": profile_id, "friend_id": friend_id}
    return friendship


def create_friendships(client: TestClient, db: Session, num_profiles: int):
    """
    Helper function to create a number of friendships
    """
    # Create the profiles
    create_profiles(client, db, num_profiles)

    # Call to create the friendships
    for i in range(1, num_profiles):
        for j in range(i+1, num_profiles+1):
            create_friendship(client, i, j)
