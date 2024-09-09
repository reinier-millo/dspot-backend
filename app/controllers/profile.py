"""
Logic for managing profiles.
"""
import math
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from app.controllers.db_types import OrderEnum, ProfileOrderFieldEnum
from app.db.models import Profile as ProfileModel, friendship
from app.models.profile import ProfileBase, ProfileResponse, PaginatedProfileResponse


class Profile:
    """
    Logic for managing profiles.
    """

    @staticmethod
    async def create(db: Session, profile: ProfileBase) -> ProfileModel:
        """
        Create a new profile
        """
        db_profile = ProfileModel(
            img=profile.img,
            first_name=profile.first_name,
            last_name=profile.last_name,
            phone=profile.phone,
            address=profile.address,
            city=profile.city,
            state=profile.state,
            zipcode=profile.zipcode,
            available=profile.available
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    async def get_all(  # pylint: disable=too-many-arguments, too-many-locals
        db: Session,
        base_url: str,
        q: str = None,
        skip: int = 0,
        limit: int = 10,
        field: ProfileOrderFieldEnum = ProfileOrderFieldEnum.CREATED_AT,
        order: OrderEnum = OrderEnum.ASC
    ) -> PaginatedProfileResponse:
        """
        Get all profiles using pagination
        """
        query = db.query(ProfileModel)

        # Filter profiles by name or last name
        if q:
            query = query.filter(
                ProfileModel.first_name.ilike(f"%{q}%") |
                ProfileModel.last_name.ilike(f"%{q}%")
            )

        # Order profiles result by field and order
        order_func = asc if order == OrderEnum.ASC else desc
        query = query.order_by(order_func(getattr(ProfileModel, field.value)))

        # Get total of profiles for pagination
        total = query.count()

        # Ensure skip is not greater than total
        if skip >= total:
            base_mult = math.floor(total / limit)
            skip = limit * base_mult

        # Get profiles data
        profiles_db = query.offset(skip).limit(limit).all()
        profiles = [ProfileResponse.model_validate(
            profile) for profile in profiles_db]

        # Get next and previous page urls
        next_skip = skip + limit
        next_url = f"{base_url}?{f'q={q}&' if q else ''}skip={next_skip}&limit={limit}&field={field.value}&order={order.value}" if next_skip < total else None  # pylint: disable=line-too-long
        previous_skip = skip - limit
        previous_url = f"{base_url}?{f'q={q}&' if q else ''}skip={previous_skip}&limit={limit}&field={field.value}&order={order.value}" if previous_skip >= 0 else None  # pylint: disable=line-too-long

        # Return paginated profiles
        return PaginatedProfileResponse(
            total=total,
            next_url=next_url,
            previous_url=previous_url,
            profiles=profiles,
        )

    @staticmethod
    async def get(db: Session, profile_id: int) -> ProfileModel | None:
        """
        Get a profile by id
        """
        return db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()

    @staticmethod
    async def update(db: Session, profile_id: int, profile: ProfileBase) -> ProfileModel | None:
        """
        Update a profile by id
        """
        db_profile = db.query(ProfileModel).filter(
            ProfileModel.id == profile_id).first()
        if db_profile:
            db_profile.img = profile.img
            db_profile.first_name = profile.first_name
            db_profile.last_name = profile.last_name
            db_profile.phone = profile.phone
            db_profile.address = profile.address
            db_profile.city = profile.city
            db_profile.state = profile.state
            db_profile.zipcode = profile.zipcode
            db_profile.available = profile.available
            db.commit()
            db.refresh(db_profile)
            return db_profile
        return None

    @staticmethod
    async def delete(db: Session, profile_id: int) -> ProfileModel | None:
        """
        Delete a profile by id
        """
        db_profile = db.query(ProfileModel).filter(
            ProfileModel.id == profile_id).first()
        if db_profile:
            db.delete(db_profile)
            db.commit()
            return db_profile
        return None

    @staticmethod
    async def get_friends(  # pylint: disable=too-many-locals
        db: Session,
        profile_id: int,
        base_url: str,
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedProfileResponse:
        """
        Get all friends of a profile by id
        """
        # Subquery to get friend IDs
        friend_ids_select = select(friendship.c.friend_id).where(
            friendship.c.profile_id == profile_id)
        inverse_friend_ids_select = select(friendship.c.profile_id).where(
            friendship.c.friend_id == profile_id)

        # Query to get friend profiles
        query = db.query(ProfileModel).filter(
            ProfileModel.id.in_(friend_ids_select) |
            ProfileModel.id.in_(inverse_friend_ids_select))

        # Get total number of friends for pagination
        total = query.count()

        # Ensure skip is not greater than total
        if skip >= total:
            base_mult = math.floor(total / limit)
            skip = limit * base_mult

        # Get friends data
        friends_db = query.offset(skip).limit(limit).all()
        friends_list = [ProfileResponse.model_validate(
            friend) for friend in friends_db]

        # Get next and previous page urls
        next_skip = skip + limit
        next_url = f"{base_url}?skip={next_skip}&limit={limit}" if next_skip < total else None
        previous_skip = skip - limit
        previous_url = f"{base_url}?skip={previous_skip}&limit={limit}" if previous_skip >= 0 else None

        # Return paginated friends
        return PaginatedProfileResponse(
            total=total,
            next_url=next_url,
            previous_url=previous_url,
            profiles=friends_list,
        )
