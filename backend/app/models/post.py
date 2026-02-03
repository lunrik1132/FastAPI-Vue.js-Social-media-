from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import pytz


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    date_created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
    )

    author = relationship(
        "User", foreign_keys=[author_id], back_populates="authored_posts"
    )
    destination = relationship(
        "User", foreign_keys=[destination_id], back_populates="received_posts"
    )

    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
