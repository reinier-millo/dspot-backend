"""
Predefined constants for testing 
"""

PROFILES_TO_CREATE = 100
PROFILES_TO_UPDATE = 50
PROFILES_TO_DELETE = 15
AFTER_DELETE_PROFILES = PROFILES_TO_CREATE - PROFILES_TO_DELETE
NON_VALID_PROFILE_ID = PROFILES_TO_CREATE + 1
PROFILES_FRIENDSHIPS_TO_CREATE = 10

PROFILE_DATA = {
    "img": "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
    "first_name": "Steph",
    "last_name": "Walters",
    "phone": "(820) 289-1818",
    "address": "5190 Center Court Drive",
    "city": "Spring",
    "state": "TX",
    "zipcode": "77370",
    "available": True
}
