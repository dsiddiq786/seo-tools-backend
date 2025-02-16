from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from app.db.session import Base

class APILog(Base):
    """
    ✅ Logs every API call with user details, timestamps, and performance metrics
    """
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Guest users won't have a user_id
    tool_name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=func.now())
    response_time = Column(Float, nullable=True)
    request_payload = Column(String, nullable=True)
    response_status = Column(Integer, nullable=True)