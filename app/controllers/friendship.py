from app.db.models import Profile, friendship
from sqlalchemy import select, delete
from sqlalchemy.orm import Session


class Friendship:
    @staticmethod
    def exists(db: Session, profile_id: int, friend_id: int):
        """
        Check if a friendship relationship exists
        """
        stmt = select(friendship).where(
            friendship.c.profile_id == profile_id,
            friendship.c.friend_id == friend_id
        )
        relationship = db.execute(stmt).first()
        return relationship is not None

    @staticmethod
    def create(db: Session, profile_id: int, friend_id: int):
        """
        Create a new friendship relationship
        """
        # Check that both profiles exist
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return (None, friend_id)
        friend = db.query(Profile).filter(Profile.id == friend_id).first()
        if not friend:
            return (profile_id, None)

        # Check that the friendship relationship doesn't already exist
        if Friendship.exists(db, profile_id, friend_id):
            return (profile_id, friend_id)

        # Create the friendship relationship
        profile.friends.append(friend)
        db.add(profile)
        db.commit()
        return (profile_id, friend_id)

    @staticmethod
    def delete(db: Session, profile_id: int, friend_id: int):
        """
        Delete a friendship relationship
        """
        if not Friendship.exists(db, profile_id, friend_id):
            return False

        # Delete the friendship relationship
        stmt = delete(friendship).where(
            friendship.c.profile_id == profile_id,
            friendship.c.friend_id == friend_id
        )
        db.execute(stmt)
        db.commit()
        return True
