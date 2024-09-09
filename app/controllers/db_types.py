from enum import Enum


class OrderEnum(str, Enum):
    """
    Order allowed values
    """
    asc = "asc"
    desc = "desc"


class ProfileOrderFieldEnum(str, Enum):
    """
    Profile order field allowed values
    """
    first_name = "first_name"
    city = "city"
    state = "state"
    zipcode = "zipcode"
    created_at = "created_at"
    updated_at = "updated_at"
