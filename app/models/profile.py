from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class ProfileBase(BaseModel):
    img: str = Field(..., description="The image of the profile")
    first_name: str = Field(..., description="The first name of the profile")
    last_name: str = Field(..., description="The last name of the profile")
    phone: str = Field(..., description="The phone of the profile")
    address: Optional[str] = Field(None, description="The address of the profile")
    city: Optional[str] = Field(None, description="The city of the profile")
    state: Optional[str] = Field(None, description="The state of the profile")
    zipcode: Optional[str] = Field(None, description="The zipcode of the profile")
    available: Optional[bool] = Field(True, description="Indicate if the profile is available to be friend")

class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="The ID of the profile")
    created_at: datetime = Field(..., description="Date/Time when profile was created")
    updated_at: datetime = Field(..., description="Date?Time for the last profile update")


class PaginatedProfileResponse(BaseModel):
    total: int = Field(..., description="Total number of profiles")
    next_url: Optional[str] = Field(None, description="Next page url")
    previous_url: Optional[str] = Field(None, description="Previous page url")
    profiles: List[ProfileResponse] = Field(..., description="The list of profiles")