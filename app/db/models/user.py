from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    account_type = Column(String, default="guest")  # guest, free, pro
    remaining_tokens = Column(Integer, default=100)  # Initial token allocation
    subscription_status = Column(String, default="inactive")  # active, inactive, expired
    subscription_expiry = Column(DateTime, nullable=True)  # Subscription expiration date
    token_refresh_date = Column(DateTime, default=datetime.utcnow)  # Token reset schedule
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationship using `back_populates` (Deferred import in `api_usage.py`)
    api_usage = relationship("APIUsage", back_populates="user", cascade="all, delete-orphan")