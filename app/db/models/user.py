from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    account_type = Column(String, default="guest")  # guest, free, pro
    remaining_tokens = Column(Integer, default=100)  # Initial token allocation
    subscription_status = Column(String, default="inactive")  # active, inactive, expired
    subscription_expiry = Column(DateTime, nullable=True)  # Subscription expiration date
    token_refresh_date = Column(DateTime, default=datetime.utcnow)  # Token reset schedule
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    api_usage = relationship("APIUsage", back_populates="user")

User.payments = relationship("Payment", back_populates="user")
    
