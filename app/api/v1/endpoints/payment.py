from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.payment import Payment
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta

router = APIRouter()

class PaymentRequest(BaseModel):
    user_id: int
    plan_name: str  # free, pro, enterprise
    amount: float

@router.post("/subscribe")
def process_payment(payment_request: PaymentRequest, db: Session = Depends(SessionLocal)):
    """
    ✅ Process Payment and Activate Subscription
    """
    user = db.query(User).filter(User.id == payment_request.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Generate Unique Transaction ID
    transaction_id = str(uuid.uuid4())

    # ✅ Save Payment Record
    payment = Payment(
        user_id=user.id,
        plan_name=payment_request.plan_name,
        amount=payment_request.amount,
        payment_status="completed",
        transaction_id=transaction_id
    )
    db.add(payment)

    # ✅ Update User Subscription
    user.account_type = payment_request.plan_name
    user.subscription_status = "active"
    user.subscription_expiry = datetime.utcnow() + timedelta(days=30)  # 30-day subscription

    if payment_request.plan_name == "pro":
        user.remaining_tokens = 100
    elif payment_request.plan_name == "enterprise":
        user.remaining_tokens = 500

    db.commit()

    return {"message": "Subscription activated", "transaction_id": transaction_id}