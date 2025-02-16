from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
import datetime

class APIUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Link API calls to a user
    tool_name = Column(String, index=True)
    used_calls = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # ✅ Relationship using `back_populates` (Deferred import in `user.py`)
    user = relationship("User", back_populates="api_usage")