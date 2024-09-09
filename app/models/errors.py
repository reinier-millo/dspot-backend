from pydantic import BaseModel, Field


class ProfileNotFoundError(BaseModel):
    error: str = Field("profile-not-found", description="The error code")
