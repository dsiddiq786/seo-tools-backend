from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserResponse
from app.db.session import get_db

router = APIRouter()

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Retrieve all users."""
    return db.query(User).all()

@router.post("/users")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    """Create a new user."""
    new_user = User(username=username, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
