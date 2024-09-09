import json
import argparse
import random
import logging
from app.db.config import SessionLocal
from app.db.models import Profile

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_items_from_text_file(file_path: str) -> list[str]:
    """
    Load the items from text file to be used for profile generation
    """
    items = []
    with open(file_path, "r") as f:
        items = [line.strip() for line in f.readlines()]
    return items


def load_items_from_json_file(file_path: str) -> dict:
    """
    Load the items from JSON to be used for profile generation
    """
    items = {}
    with open(file_path, "r") as f:
        items = json.load(f)
    return items


def gen_profile_picture() -> str:
    """
    Generate the profile picture
    """
    picture_id = random.randint(10000, 150000)
    return f"https://images.pexels.com/photos/{picture_id}/pexels-photo-{picture_id}.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"


def gen_phone_number() -> str:
    """
    Generate the phone number
    """
    area_code = random.randint(100, 999)
    office_code = random.randint(100, 999)
    line_code = random.randint(1000, 9999)
    return f"({area_code}) {office_code}-{line_code}"


def gen_friend_relationship(max_profiles: int) -> tuple[int, int]:
    """
    Generate the friend relationship pair
    """
    profile_idx = random.randint(0, max_profiles)
    friend_idx = random.randint(0, max_profiles)

    # Ensure that the profile and friend are not the same
    while profile_idx == friend_idx:
        friend_idx = random.randint(0, max_profiles)

    return (profile_idx, friend_idx)


def gen_profiles(total_profiles: int, total_friends: int) -> list[dict]:
    """
    Generate the profiles
    """
    db = SessionLocal()
    logger.info("Loading required data")
    names = load_items_from_text_file("data/names.txt")
    lastnames = load_items_from_text_file("data/lastnames.txt")
    street_names = load_items_from_text_file("data/street_names.txt")
    zip_to_state_city = load_items_from_json_file(
        "data/states_cities_zips.json")
    zips = list(zip_to_state_city.keys())

    # Prepare the new profiles to be generated
    logger.info("Start profiles generation")
    profiles: list[Profile] = []
    for i in range(total_profiles):
        zip = random.choice(zips)
        profile = Profile(
            img=gen_profile_picture(),
            first_name=random.choice(names),
            last_name=random.choice(lastnames),
            phone=gen_phone_number(),
            address=f"{random.randint(1000,9000)} {random.choice(street_names)}",
            city=zip_to_state_city.get(zip).get("city"),
            state=zip_to_state_city.get(zip).get("state"),
            zipcode=zip,
            available=True
        )
        profiles.append(profile)

    # Prepare the friend relationships
    logger.info("Start friend relationships generation")
    max_idx = total_profiles - 1
    generated_friends = []
    for i in range(total_friends):
        # Look for the random profile and friend
        (profile_idx, friend_idx) = gen_friend_relationship(max_idx)
        key = f"{profile_idx}-{friend_idx}"

        # Prevent duplicate friend relationships
        while key in generated_friends:
            (profile_idx, friend_idx) = gen_friend_relationship(max_idx)
            key = f"{profile_idx}-{friend_idx}"
        generated_friends.append(key)

        # Attach the friend relationship
        profiles[profile_idx].friends.append(profiles[friend_idx])

    # Persists the new profiles in the database
    db.add_all(profiles)
    db.commit()
    logger.info(
        f"{total_profiles} profiles and {total_friends} friend relationships generated successfully")


if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="Generate random profiles")
    parser.add_argument("--total_profiles", type=int, default=100)
    parser.add_argument("--total_friends", type=int, default=150)
    args = parser.parse_args()

    # Call to generate the random profiles
    gen_profiles(args.total_profiles, args.total_friends)
