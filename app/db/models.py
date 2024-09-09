"""
Database models
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.config import Base

# Define the many-to-many friendship relationship table
friendship = Table(
    "friendship",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey(
        "profiles.id"), index=True, primary_key=True),
    Column("friend_id", Integer, ForeignKey(
        "profiles.id"), index=True, primary_key=True),
    Column("created_at", DateTime, server_default=func.now(),  # pylint: disable=not-callable
           index=True)
)


class Profile(Base):  # pylint: disable=too-few-public-methods
    """
    Profile model
    """
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    img = Column(String)
    first_name = Column(String, index=True)
    last_name = Column(String)
    phone = Column(String)
    address = Column(String, nullable=True)
    city = Column(String, index=True, nullable=True)
    state = Column(String, index=True, nullable=True)
    zipcode = Column(String, index=True, nullable=True)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(),  # pylint: disable=not-callable
                        index=True)
    updated_at = Column(DateTime, server_default=func.now(),  # pylint: disable=not-callable
                        server_onupdate=func.now(), index=True)  # pylint: disable=not-callable

    friends = relationship(
        "Profile",
        secondary=friendship,
        primaryjoin=id == friendship.c.profile_id,
        secondaryjoin=id == friendship.c.friend_id,
        backref="friend_of"
    )
