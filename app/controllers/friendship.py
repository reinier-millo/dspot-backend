from app.db.models import Profile, friendship
from collections import deque
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
    async def create(db: Session, profile_id: int, friend_id: int):
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
    async def delete(db: Session, profile_id: int, friend_id: int):
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

    @staticmethod
    def get_all_friends(db: Session, profile_id: int) -> list[int]:
        """
        Get all friends of a profile by id
        """
        friend_ids_stmt = (
            select(friendship.c.friend_id)
            .where(friendship.c.profile_id == profile_id)
            .union(
                select(friendship.c.profile_id)
                .where(friendship.c.friend_id == profile_id)
            )
        )
        return db.scalars(friend_ids_stmt).all()

    @staticmethod
    async def get_connection(db: Session, profile_id: int, friend_id: int) -> list[int]:
        """
        Get the shorter connection between two profiles applying Breadth First Search algorithm
        """
        # Initialize the queue with the starting profile
        queue = deque([(profile_id, [profile_id])])
        visited = set()

        # Perform BFS
        while queue:
            current_profile, path = queue.popleft()
            if current_profile == friend_id:
                return path
            if current_profile not in visited:
                visited.add(current_profile)
                friends = Friendship.get_all_friends(db, current_profile)
                for friend in friends:
                    if friend not in visited:
                        queue.append((friend, path + [friend]))
        return []
