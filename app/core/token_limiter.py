from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.api_usage import APIUsage
from app.core.security import decode_jwt
import hashlib
import uuid
import time
from datetime import datetime

# ✅ Request tracking
request_timestamps = {}

# ✅ Known bot user-agents
BOT_USER_AGENTS = ["bot", "spider", "crawler", "scraper"]

class TokenLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        ✅ Correctly differentiates between logged-in users and guests
        ✅ Prevents duplicate guest creation for the same machine
        ✅ Ensures guest users are upgraded upon login
        ✅ Blocks bots and applies rate limits
        """

        db: Session = SessionLocal()

        # ✅ Bypass rate limiting for public routes
        public_routes = ["/docs", "/openapi.json", "/auth/", "/users/", "/health", "/payment/subscribe"]
        if any(request.url.path.startswith(route) for route in public_routes):
            return await call_next(request)

        # ✅ Block bot traffic
        user_agent = request.headers.get("User-Agent", "").lower()
        if any(bot in user_agent for bot in BOT_USER_AGENTS):
            return JSONResponse(status_code=403, content={"status": "error", "message": "Bot traffic is not allowed."})

        # ✅ Rate-limit based on IP
        client_ip = request.client.host
        current_time = time.time()

        if client_ip in request_timestamps:
            last_request_time = request_timestamps[client_ip]
            if current_time - last_request_time < 1:  # 1 request per second limit
                return JSONResponse(status_code=429, content={"status": "error", "message": "Too many requests. Slow down!"})

        request_timestamps[client_ip] = current_time  # ✅ Store request timestamp

        # ✅ Check for JWT Authorization First (Prioritize over guest detection)
        auth_header = request.headers.get("Authorization")
        user = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                user_data = decode_jwt(token)
                user = db.query(User).filter(User.id == user_data["id"]).first()

                # ✅ If the user was previously a guest, upgrade them
                if user and user.account_type == "guest":
                    user.account_type = "free"  # Upgrade to Free Plan
                    user.remaining_tokens = 20  # Assign new quota
                    user.subscription_status = "active"
                    db.commit()

            except Exception:
                pass  # Invalid or expired token

        # ✅ Unique Guest Identifier (IP + User-Agent Hash)
        unique_identifier = hashlib.sha256(f"{client_ip}-{user_agent}".encode()).hexdigest()

        # ✅ If No Auth Token and No User Found → Check Guest Profile
        if not user:
            existing_guest = db.query(User).filter(User.username == unique_identifier).first()

            if not existing_guest:
                # ✅ Create a new guest user only if no token was provided
                user = User(
                    username=unique_identifier,
                    account_type="guest",
                    remaining_tokens=10,
                    subscription_status="inactive",
                    subscription_expiry=None
                )
                db.add(user)
                db.commit()
            else:
                user = existing_guest

        # ✅ Check Subscription Expiry (For Logged-in Users)
        if user.account_type != "guest" and user.subscription_expiry:
            if user.subscription_expiry < datetime.utcnow():
                user.subscription_status = "expired"
                db.commit()
                return JSONResponse(status_code=403, content={"status": "error", "message": "Subscription expired. Please renew."})

        # ✅ Determine API limits based on user type
        user_limits = {"guest": 10, "free": 20, "pro": 100, "enterprise": 500}
        allowed_calls = user_limits.get(user.account_type, 10)

        # ✅ Track API Usage for Each Tool
        tool_name = request.url.path.split("/")[-1]
        api_usage = db.query(APIUsage).filter_by(user_id=user.id, tool_name=tool_name).first()

        if not api_usage:
            api_usage = APIUsage(user_id=user.id, tool_name=tool_name, used_calls=0)
            db.add(api_usage)
            db.commit()

        # ✅ Enforce API limits
        if api_usage.used_calls >= allowed_calls:
            db.close()
            message = (
                "API limit exceeded! Sign up to continue." if user.account_type == "guest" 
                else "API limit exceeded! Upgrade to Pro for more calls." if user.account_type == "free" 
                else "API limit exhausted! Upgrade your plan."
            )
            return JSONResponse(status_code=429, content={"status": "error", "message": message})

        # ✅ Deduct API call
        api_usage.used_calls += 1
        db.commit()
        db.close()

        return await call_next(request)