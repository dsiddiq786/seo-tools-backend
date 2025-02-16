from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.session import get_db
from passlib.context import CryptContext
from pydantic import BaseModel
from app.core.security import hash_password, verify_password, create_jwt, create_refresh_token,decode_jwt

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    ✅ Converts a guest user into a full registered user.
    ✅ Keeps their API usage intact.
    """

    # ✅ Check if user exists as a guest
    user = db.query(User).filter(User.username.startswith("guest_"), User.email == request.email).first()

    if user:
        # ✅ Upgrade guest user to registered
        user.username = request.username
        user.hashed_password = hash_password(request.password)
        user.account_type = "free"  # Start with free plan
        db.commit()
        return {"message": "Account upgraded successfully!"}

    # ✅ If not a guest, create a new user
    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password),
        account_type="free",
        remaining_tokens=20  # Free users start with 20 tokens
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully!"}

@router.post("/login", response_model=LoginResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """
    ✅ Secure Login API
    ✅ Issues JWT Token & Refresh Token
    """
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Generate JWT & Refresh Token
    access_token = create_jwt({"id": user.id, "email": user.email})
    refresh_token = create_refresh_token({"id": user.id, "email": user.email})

    return LoginResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh-token")
def refresh_token(request: RefreshTokenRequest):
    """
    ✅ Allows users to refresh access tokens
    """
    decoded_token = decode_jwt(request.refresh_token)

    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = create_jwt({"id": decoded_token["id"], "email": decoded_token["email"]})
    return {"access_token": new_access_token, "token_type": "bearer"}
