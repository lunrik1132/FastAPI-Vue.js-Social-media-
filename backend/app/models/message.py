from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import pytz


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(
        Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    sender_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    text = Column(Text, nullable=False)
    date_created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
    )
    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")
