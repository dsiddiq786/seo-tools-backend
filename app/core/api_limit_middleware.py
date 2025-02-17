from fastapi import Request, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.api_usage import APIUsage
from app.db.models.user import User
from app.core.security import get_mac_address
import datetime

class APILimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware to track and limit API usage based on user type (Guest, Free, Pro).
        """

        # Get user IP & MAC Address
        ip_address = request.client.host
        mac_address = get_mac_address(ip_address)

        # Start DB session
        db: Session = SessionLocal()

        # Check if user is logged in (JWT Authorization)
        user = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user = db.query(User).filter(User.token == token).first()

        # Determine user type & API limits
        if user:
            user_type = user.account_type  # free / pro
            allowed_calls = 20 if user_type == "free" else 100
        else:
            user_type = "guest"
            allowed_calls = 10  # Guest users get 10 free calls

        # Check API usage in database
        api_usage = db.query(APIUsage).filter_by(ip_address=ip_address, mac_address=mac_address).first()

        if not api_usage:
            api_usage = APIUsage(ip_address=ip_address, mac_address=mac_address, user_type=user_type, used_calls=0)
            db.add(api_usage)
            db.commit()

        # If limit is exceeded
        if api_usage.used_calls >= allowed_calls:
            if user_type == "guest":
                raise HTTPException(status_code=429, detail="API limit exceeded! Please sign up to continue.")
            elif user_type == "free":
                raise HTTPException(status_code=429, detail="API limit exceeded! Upgrade to Pro for more calls.")
            else:
                raise HTTPException(status_code=429, detail="API limit exhausted! Upgrade your plan.")

        # Increment API call count
        api_usage.used_calls += 1
        db.commit()

        # Continue processing request
        response = await call_next(request)

        # Close DB session
        db.close()

        return response