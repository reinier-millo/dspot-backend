"""
Routes for the friendship
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from app.constants import PROFILE_NOT_FOUND, FRIEND_NOT_FOUND, FRIENDSHIP_NOT_FOUND, FRIENDSHIP_SAME_PROFILE
from app.controllers.friendship import Friendship
from app.db.config import get_db
from app.models.friendship import FriendshipBase, FriendshipConnectionResponse


friendship_router = APIRouter(prefix="/friendship", tags=["friendship"])


@friendship_router.post(
    "/create",
    response_model=FriendshipBase,
    status_code=201,
    summary="Create a new friendship relationship",
    description="Create a new friendship relationship",
    response_description="Return the new created friendship relationship"
)
async def create_friendship(
    relationship: FriendshipBase = Body(
        description="The new friendship relationship data"),
    db: Session = Depends(get_db)
):
    """
    Create a new friendship relationship
    """
    if relationship.profile_id == relationship.friend_id:
        raise HTTPException(status_code=400, detail=FRIENDSHIP_SAME_PROFILE)

    (profile_id, friend_id) = await Friendship.create(
        db, relationship.profile_id, relationship.friend_id)
    if profile_id is None:
        raise HTTPException(status_code=404, detail=PROFILE_NOT_FOUND)
    if friend_id is None:
        raise HTTPException(status_code=404, detail=FRIEND_NOT_FOUND)
    return relationship


@friendship_router.delete(
    "/{profile_id}/{friend_id}/delete",
    response_model=FriendshipBase,
    status_code=200,
    summary="Delete a friendship relationship",
    description="Delete a friendship relationship",
    response_description="Return the deleted friendship relationship"
)
async def delete_friend(
    profile_id: int = Path(description="The profile id"),
    friend_id: int = Path(description="The friend id"),
    db: Session = Depends(get_db)
):
    """
    Delete a friendship relationship
    """
    deleted = await Friendship.delete(db, profile_id, friend_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=FRIENDSHIP_NOT_FOUND)
    return {"profile_id": profile_id, "friend_id": friend_id}


@friendship_router.get(
    "/{profile_id}/{friend_id}/connection",
    response_model=FriendshipConnectionResponse,
    status_code=200,
    summary="Get the shorter connection between two profiles",
    description="Get the shorter connection between two profiles applying Breadth First Search algorithm",
    response_description="Return the shorter connection between the two profiles"
)
async def get_connection_level(
    profile_id: int = Path(description="The profile id"),
    friend_id: int = Path(description="The friend id"),
    db: Session = Depends(get_db)
):
    """
    Get the shorter connection between two profiles
    """
    connection = await Friendship.get_connection(db, profile_id, friend_id)
    return {"path": connection}
