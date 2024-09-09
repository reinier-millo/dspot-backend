from pydantic import BaseModel, Field


class ProfileNotFoundError(BaseModel):
    error: str = Field("profile-not-found", description="The error code")

class FriendNotFoundError(BaseModel):
    error: str = Field("friend-profile-not-found", description="The error code")

class FriendRelationshipNotFoundError(BaseModel):
    error: str = Field("friend-relationship-not-found", description="The error code")
