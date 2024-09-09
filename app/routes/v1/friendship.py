from fastapi import APIRouter, Depends, HTTPException, Path, Body
from app.controllers.friendship import Friendship
from app.db.config import get_db
from sqlalchemy.orm import Session
from app.models.friendship import FriendshipBase
from app.models.errors import PROFILE_NOT_FOUND, FRIEND_NOT_FOUND, FRIENDSHIP_NOT_FOUND, FRIENDSHIP_SAME_PROFILE


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

    (profile_id, friend_id) = Friendship.create(
        db, relationship.profile_id, relationship.friend_id)
    if profile_id is None:
        raise HTTPException(status_code=404, detail=PROFILE_NOT_FOUND)
    if friend_id is None:
        raise HTTPException(status_code=404, detail=FRIEND_NOT_FOUND)
    return relationship


@friendship_router.delete(
    "/{profile_id}/{friend_id}/delete",
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
    deleted = Friendship.delete(db, profile_id, friend_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=FRIENDSHIP_NOT_FOUND)
    return {"profile_id": profile_id, "friend_id": friend_id}
