from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User, APIUsage
from app.core.security import decode_jwt
import uuid
import time
from datetime import datetime

# ✅ Store last request timestamps to prevent abuse
request_timestamps = {}

# ✅ Known bot user-agents
BOT_USER_AGENTS = ["bot", "spider", "crawler", "scraper"]

class TokenLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        ✅ Blocks known bot user-agents
        ✅ Rate-limits repeated requests from the same IP
        ✅ Enforces API usage limits based on user type and subscription
        ✅ Tracks usage per tool
        ✅ Enforces subscription expiration checks
        """

        # ✅ Public routes (Don't enforce limits)
        public_routes = ["/docs", "/openapi.json", "/auth/", "/users/", "/health", "/payment/subscribe"]
        if any(request.url.path.startswith(route) for route in public_routes):
            return await call_next(request)

        # ✅ Block bot user-agents
        user_agent = request.headers.get("User-Agent", "").lower()
        if any(bot in user_agent for bot in BOT_USER_AGENTS):
            raise HTTPException(status_code=403, detail="Bot traffic is not allowed.")

        # ✅ Rate-limit based on IP
        client_ip = request.client.host
        current_time = time.time()

        if client_ip in request_timestamps:
            last_request_time = request_timestamps[client_ip]
            if current_time - last_request_time < 1:  # 1 request per second limit
                raise HTTPException(status_code=429, detail="Too many requests. Slow down!")

        request_timestamps[client_ip] = current_time  # ✅ Store request timestamp

        # ✅ Start DB session
        db: Session = SessionLocal()

        # ✅ Check for JWT Authorization
        auth_header = request.headers.get("Authorization")
        user = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                user_data = decode_jwt(token)
                user = db.query(User).filter(User.id == user_data["id"]).first()
            except Exception:
                pass  # Invalid or expired token

        # ✅ If no user is found, create a guest user (Temporary Users)
        if not user:
            guest_username = f"guest_{uuid.uuid4().hex[:8]}"  # Generate unique guest username
            user = db.query(User).filter(User.username == guest_username).first()

            if not user:
                user = User(
                    username=guest_username,
                    account_type="guest",
                    remaining_tokens=10,  # Guest Users get 10 API calls
                    subscription_status="inactive",
                    subscription_expiry=None
                )
                db.add(user)
                db.commit()

        # ✅ Check Subscription Expiry (For Logged-in Users)
        if user.account_type != "guest" and user.subscription_expiry:
            if user.subscription_expiry < datetime.utcnow():
                user.subscription_status = "expired"
                db.commit()
                raise HTTPException(status_code=403, detail="Subscription expired. Please renew.")

        # ✅ Determine API limits based on user type
        user_limits = {"guest": 10, "free": 20, "pro": 100, "enterprise": 500}
        allowed_calls = user_limits.get(user.account_type, 10)  # Default to guest

        # ✅ Track API Usage for Each Tool
        tool_name = request.url.path.split("/")[-1]  # Extract tool name
        api_usage = db.query(APIUsage).filter_by(user_id=user.id, tool_name=tool_name).first()

        if not api_usage:
            api_usage = APIUsage(user_id=user.id, tool_name=tool_name, used_calls=0)
            db.add(api_usage)
            db.commit()

        # ✅ If API limit is exceeded
        if api_usage.used_calls >= allowed_calls:
            db.close()
            if user.account_type == "guest":
                raise HTTPException(status_code=429, detail="API limit exceeded! Sign up to continue.")
            elif user.account_type == "free":
                raise HTTPException(status_code=429, detail="API limit exceeded! Upgrade to Pro for more calls.")
            else:
                raise HTTPException(status_code=429, detail="API limit exhausted! Upgrade your plan.")

        # ✅ Deduct API call and commit usage
        api_usage.used_calls += 1
        db.commit()
        db.close()

        return await call_next(request)