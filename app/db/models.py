from app.db.config import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Define the many-to-many friend relationship table
friends = Table(
    "friends",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey(
        "profiles.id"), index=True, primary_key=True),
    Column("friend_id", Integer, ForeignKey(
        "profiles.id"), index=True, primary_key=True),
    Column("created_at", DateTime, server_default=func.now(), index=True)
)


class Profile(Base):
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
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(),
                        server_onupdate=func.now(), index=True)

    friends = relationship(
        "Profile",
        secondary=friends,
        primaryjoin=id == friends.c.profile_id,
        secondaryjoin=id == friends.c.friend_id,
        backref="friend_of"
    )
