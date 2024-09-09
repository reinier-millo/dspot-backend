"""
Enums for the database types.
"""
from enum import Enum


class OrderEnum(str, Enum):
    """
    Order allowed values
    """
    ASC = "asc"
    DESC = "desc"


class ProfileOrderFieldEnum(str, Enum):
    """
    Profile order field allowed values
    """
    FIRST_NAME = "first_name"
    CITY = "city"
    STATE = "state"
    ZIPCODE = "zipcode"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
