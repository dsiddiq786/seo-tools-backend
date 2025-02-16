from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import SessionLocal
from app.db.models.user import User

router = APIRouter()

@router.get("/subscription-status/{user_id}")
def check_subscription(user_id: int, db: Session = Depends(SessionLocal)):
    """
    ✅ Check if User Subscription is Active or Expired
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.subscription_expiry and user.subscription_expiry < datetime.utcnow():
        user.subscription_status = "expired"
        db.commit()
        return {"message": "Subscription expired", "status": "expired"}

    return {"message": "Subscription is active", "status": user.subscription_status}