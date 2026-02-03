from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import pytz


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    description = Column(Text)
    gender = Column(Integer)
    birthday = Column(DateTime)
    country = Column(String)
    date_created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
    )

    authored_posts = relationship(
        "Post",
        foreign_keys="Post.author_id",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    received_posts = relationship(
        "Post",
        foreign_keys="Post.destination_id",
        back_populates="destination",
        cascade="all, delete-orphan",
    )
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )

    sent_friend_requests = relationship(
        "Friendship",
        foreign_keys="Friendship.requester_id",
        back_populates="requester",
        cascade="all, delete-orphan",
    )

    received_friend_requests = relationship(
        "Friendship",
        foreign_keys="Friendship.addressee_id",
        back_populates="addressee",
        cascade="all, delete-orphan",
    )
    chat_members = relationship(
        "ChatMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    sent_messages = relationship(
        "Message",
        back_populates="sender",
        cascade="all, delete-orphan",
    )
