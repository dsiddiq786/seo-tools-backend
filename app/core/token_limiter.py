from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import decode_jwt

class TokenLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define public routes that don't require token validation
        public_routes = ["/docs", "/openapi.json", "/auth/", "/tools/", "/users"]
        if any(request.url.path.startswith(route) for route in public_routes):
            return await call_next(request)

        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token header")

        # Decode JWT token
        token = auth_header.split(" ")[1]
        user_data = decode_jwt(token)
        if not user_data:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

        # Fetch user from database
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_data["id"]).first()
            if not user or not user.is_active:
                raise HTTPException(status_code=403, detail="Forbidden: User is inactive or does not exist")

            # Check remaining tokens
            if user.remaining_tokens <= 0:
                raise HTTPException(status_code=429, detail="Too many requests: Token limit exceeded")

            # Deduct one token
            user.remaining_tokens -= 1
            db.commit()

        finally:
            db.close()

        # Proceed to the next middleware or endpoint
        return await call_next(request)
