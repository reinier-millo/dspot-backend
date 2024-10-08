"""
Routes for the profile
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, Request
from sqlalchemy.orm import Session
from app.controllers.db_types import OrderEnum, ProfileOrderFieldEnum
from app.controllers.profile import Profile
from app.constants import PROFILE_NOT_FOUND
from app.db.config import get_db
from app.models.profile import ProfileBase, ProfileResponse, PaginatedProfileResponse


profile_router = APIRouter(prefix="/profile", tags=["profile"])


@profile_router.post(
    "/create",
    response_model=ProfileResponse,
    status_code=201,
    summary="Create a new profile",
    description="Create a new profile",
    response_description="Return the new created profile"
)
async def create_profile(
    profile: ProfileBase = Body(description="The new profile data"),
    db: Session = Depends(get_db)
):
    """
    Create a new profile
    """
    return await Profile.create(db, profile)


@profile_router.get(
    "/{profile_id}/get",
    response_model=ProfileResponse,
    status_code=200,
    summary="Get a profile",
    description="Get a profile by id",
    response_description="Return the profile data",
)
async def get_profile(
    profile_id: int = Path(description="The ID of the profile to get"),
    db: Session = Depends(get_db)
):
    """
    Get a profile by id
    """
    obj = await Profile.get(db, profile_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=PROFILE_NOT_FOUND)
    return obj


@profile_router.get(
    "/all",
    response_model=PaginatedProfileResponse,
    status_code=200,
    summary="Get all profiles",
    description="Get all profiles or the profiles filtered by name or last name",
    response_description="Return the profiles results paginated",
)
async def get_profiles(  # pylint: disable=too-many-arguments
    request: Request,
    q: str = Query(
        None, description="Search query to filter profiles by name or last name", min_length=3),
    skip: int = Query(
        0, description="Skip records to get paginated results", ge=0),
    limit: int = Query(
        10, description="Limit records to get paginated results", ge=1, le=200),
    field: ProfileOrderFieldEnum = Query(
        ProfileOrderFieldEnum.CREATED_AT, description="Sort field used to order the results"),
    order: OrderEnum = Query(
        OrderEnum.ASC, description="Sort order used to order the results"),
    db: Session = Depends(get_db)
):
    """
    Get all profiles
    """
    base_url = request.url._url.split(  # pylint: disable=protected-access
        "?")[0]
    return await Profile.get_all(db, base_url, q, skip, limit, field, order)


@profile_router.put(
    "/{profile_id}/update",
    response_model=ProfileResponse,
    status_code=200,
    summary="Update a profile",
    description="Update a profile by id",
    response_description="Return the updated profile"
)
async def update_profile(
    profile_id: int = Path(description="The ID of the profile to update"),
    profile: ProfileBase = Body(description="The profile data to update"),
    db: Session = Depends(get_db)
):
    """
    Update a profile by id
    """
    obj = await Profile.update(db, profile_id, profile)
    if obj is None:
        raise HTTPException(status_code=404, detail=PROFILE_NOT_FOUND)
    return obj


@profile_router.delete(
    "/{profile_id}/delete",
    response_model=ProfileResponse,
    status_code=200,
    summary="Delete a profile",
    description="Delete a profile by id",
    response_description="Return the deleted profile"
)
async def delete_profile(
    profile_id: int = Path(description="The ID of the profile to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a profile by id
    """
    obj = await Profile.delete(db, profile_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=PROFILE_NOT_FOUND)
    return obj


@profile_router.get(
    "/{profile_id}/friends",
    response_model=PaginatedProfileResponse,
    status_code=200,
    summary="Get all friends of a profile",
    description="Get all friends of a profile by id",
    response_description="Return the friends of the profile"
)
async def get_friends(
    request: Request,
    profile_id: int = Path(description="The ID of the profile to get friends"),
    skip: int = Query(
        0, description="Skip records to get paginated results", ge=0),
    limit: int = Query(
        10, description="Limit records to get paginated results", ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get all friends of a profile by id
    """
    base_url = request.url._url.split(  # pylint: disable=protected-access
        "?")[0]
    return await Profile.get_friends(db, profile_id, base_url, skip, limit)
