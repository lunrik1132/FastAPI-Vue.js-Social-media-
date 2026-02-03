from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import pytz


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    date_created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
    )

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
