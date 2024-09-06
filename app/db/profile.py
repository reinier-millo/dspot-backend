from app.db.config import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

# Define the many-to-many friend relationship table
friends = Table(
    "friends",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey(
        "profiles.id"), index=True, primary_key=True),
    Column("friend_id", Integer, ForeignKey(
        "profiles.id"), index=True, primary_key=True),
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
    address = Column(String)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zipcode = Column(String, index=True)
    available = Column(Boolean)

    friends = relationship(
        "Profile",
        secondary=friends,
        primaryjoin=id == friends.c.profile_id,
        secondaryjoin=id == friends.c.friend_id,
        backref="friend_of"
    )
