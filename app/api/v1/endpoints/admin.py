from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import APILog
from typing import List
from pydantic import BaseModel

router = APIRouter()

class APILogResponse(BaseModel):
    id: int
    user_id: int
    tool_name: str
    ip_address: str
    user_agent: str
    response_time: float
    response_status: int

@router.get("/logs", response_model=List[APILogResponse])
def get_api_logs(tool_name: str = None, db: Session = Depends(SessionLocal)):
    """
    ✅ Fetch API Logs
    ✅ Filter by Tool Name
    ✅ Sort by Timestamp (Latest First)
    """
    query = db.query(APILog)

    if tool_name:
        query = query.filter(APILog.tool_name == tool_name)

    logs = query.order_by(APILog.timestamp.desc()).all()

    if not logs:
        raise HTTPException(status_code=404, detail="No logs found.")

    return logs