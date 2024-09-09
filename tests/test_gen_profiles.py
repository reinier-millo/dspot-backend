import re
import random
from sqlalchemy.orm import Session
from scripts.gen_profiles import (load_items_from_text_file, load_items_from_json_file,
                                  gen_profile_picture, gen_phone_number, gen_friend_relationship, gen_profiles)
from app.db.models import Profile, friends


def test_load_items_from_text_file():
    """
    Test the load_items_from_text_file function
    """
    items = load_items_from_text_file("data/names.txt")
    assert len(items) == 200
    assert items[0] == "James"
    items = load_items_from_text_file("data/lastnames.txt")
    assert len(items) == 600
    assert items[2] == "Abbott"
    items = load_items_from_text_file("data/street_names.txt")
    assert len(items) == 100
    assert items[4] == "Oak St"


def test_load_items_from_json_file():
    """
    Test the load_items_from_json_file function
    """
    items = load_items_from_json_file("data/states_cities_zips.json")
    keys = list(items.keys())
    assert len(keys) == 38106
    assert items.get(keys[2]) == {"state": "NY", "city": "NEW YORK"}


def test_gen_profile_picture():
    """
    Test the gen_profile_picture function
    """
    picture = gen_profile_picture()
    assert picture is not None
    assert picture.startswith("https://images.pexels.com/photos")


def test_gen_phone_number():
    """
    Test the gen_phone_number function
    """
    phone_number = gen_phone_number()
    assert re.match(r"^\(\d{3}\) \d{3}-\d{4}$", phone_number) is not None


def test_gen_friend_relationship():
    """
    Test the gen_friend_relationship function
    """
    for i in range(1000):
        (profile_idx, friend_idx) = gen_friend_relationship(10)
        assert 0 <= profile_idx <= 10 and 0 <= friend_idx <= 10
        assert profile_idx != friend_idx


def test_gen_profiles(db_session: Session):
    """
    Test the gen_profiles function
    """
    num_profiles = 0
    num_friends = 0
    for i in range(10):
        new_profiles_cnt = random.randint(10, 100)
        new_friends_cnt = random.randint(5, new_profiles_cnt)
        gen_profiles(new_profiles_cnt, new_friends_cnt)
        num_profiles += new_profiles_cnt
        num_friends += new_friends_cnt
    total_profiles = db_session.query(Profile).count()
    assert total_profiles == num_profiles
    total_friends = db_session.query(friends).count()
    assert total_friends == num_friends
