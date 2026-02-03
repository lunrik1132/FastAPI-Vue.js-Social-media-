from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
import pytz


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True)

    requester_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    addressee_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    status = Column(String, default="pending")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
    )
    accepted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "requester_id",
            "addressee_id",
            name="unique_friend_request",
        ),
    )

    requester = relationship(
        "User", foreign_keys=[requester_id], back_populates="sent_friend_requests"
    )

    addressee = relationship(
        "User", foreign_keys=[addressee_id], back_populates="received_friend_requests"
    )
