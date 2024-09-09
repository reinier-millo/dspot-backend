import math
from app.db.models import Profile as ProfileModel
from app.models.profile import ProfileBase, ProfileResponse, PaginatedProfileResponse
from app.controllers.db_types import OrderEnum, ProfileOrderFieldEnum
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import List


class Profile:
    @staticmethod
    def create(db: Session, profile: ProfileBase) -> ProfileModel:
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
    def get_all(
        db: Session,
        base_url: str,
        q: str = None,
        skip: int = 0,
        limit: int = 10,
        field: ProfileOrderFieldEnum = ProfileOrderFieldEnum.created_at,
        order: OrderEnum = OrderEnum.asc
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
        order_func = asc if order == OrderEnum.asc else desc
        query = query.order_by(order_func(getattr(ProfileModel, field.value)))

        # Get total of profiles for pagination
        total = query.count()

        # Ensure skip is not greater than total
        if skip >= total:
            base_mult = math.floor(total / limit)
            skip = limit * base_mult

            if skip < 0:
                skip = 0

        # Get profiles data
        profiles_db = query.offset(skip).limit(limit).all()
        profiles = [ProfileResponse.model_validate(profile) for profile in profiles_db]

        # Get next and previous page urls
        next_skip = skip + limit
        next_url = f"{base_url}?{f'q={q}&' if q else ''}skip={next_skip}&limit={limit}&field={field}&order={order.value}" if next_skip < total else None
        previous_skip = skip - limit
        previous_url = f"{base_url}?{f'q={q}&' if q else ''}skip={previous_skip}&limit={limit}&field={field}&order={order.value}" if previous_skip >= 0 else None

        # Return paginated profiles
        return PaginatedProfileResponse(
            total=total,
            next_url=next_url,
            previous_url=previous_url,
            profiles=profiles,
        )

    @staticmethod
    def get(db: Session, profile_id: int) -> ProfileModel | None:
        """
        Get a profile by id
        """
        return db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()

    @staticmethod
    def update(db: Session, profile_id: int, profile: ProfileBase) -> ProfileModel | None:
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
    def delete(db: Session, profile_id: int) -> ProfileModel | None:
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
