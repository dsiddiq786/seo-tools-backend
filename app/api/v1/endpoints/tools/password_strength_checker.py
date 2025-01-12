from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from zxcvbn import zxcvbn
import secrets
import string

router = APIRouter()

class PasswordStrengthRequest(BaseModel):
    password: str

class PasswordStrengthResponse(BaseModel):
    score: int
    feedback: str

class PasswordGeneratorResponse(BaseModel):
    strong_password: str

@router.post("/check-password-strength", response_model=PasswordStrengthResponse)
def check_password_strength(request: PasswordStrengthRequest):
    """Check the strength of a password."""
    try:
        result = zxcvbn(request.password)
        feedback = result['feedback']['suggestions']
        feedback_message = " ".join(feedback) if feedback else "Strong password!"
        return PasswordStrengthResponse(score=result['score'], feedback=feedback_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking password strength: {e}")

@router.get("/generate-strong-password", response_model=PasswordGeneratorResponse)
def generate_strong_password():
    """Generate a strong password."""
    try:
        length = 16  # Adjust length as needed
        characters = string.ascii_letters + string.digits + string.punctuation
        strong_password = ''.join(secrets.choice(characters) for _ in range(length))
        return PasswordGeneratorResponse(strong_password=strong_password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating strong password: {e}")
