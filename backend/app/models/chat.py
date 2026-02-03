from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import pytz


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
    )
    members = relationship(
        "ChatMember", back_populates="chat", cascade="all, delete-orphan"
    )
    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )


class ChatMember(Base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(
        Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    date_created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
    )

    __table_args__ = (UniqueConstraint("chat_id", "user_id", name="unique_chat_user"),)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_members")
