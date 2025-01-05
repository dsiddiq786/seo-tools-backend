from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    account_type = Column(String, default="free")  # free, premium, enterprise
    remaining_tokens = Column(Integer, default=100)  # Initial token allocation
    token_refresh_date = Column(DateTime, default=datetime.utcnow)  # Token reset schedule
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
