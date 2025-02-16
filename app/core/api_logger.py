from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User, APILog
import time
import json

class APILoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        ✅ Logs every API call with request details and response time
        """

        # ✅ Capture request start time
        start_time = time.time()

        # ✅ Extract user data if available
        auth_header = request.headers.get("Authorization")
        user_id = None

        with SessionLocal() as db:
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                user = db.query(User).filter(User.token == token).first()
                if user:
                    user_id = user.id

        # ✅ Extract request details
        ip_address = request.client.host
        user_agent = request.headers.get("User-Agent", "Unknown")
        tool_name = request.url.path.split("/")[-1]  # Extract tool name
        request_payload = await request.body()
        request_payload = request_payload.decode("utf-8")[:500]  # Limit to 500 chars

        # ✅ Proceed with API call
        response = await call_next(request)

        # ✅ Capture response time & status
        end_time = time.time()
        response_time = round(end_time - start_time, 4)
        response_status = response.status_code

        # ✅ Log API call in DB
        with SessionLocal() as db:
            log_entry = APILog(
                user_id=user_id,
                tool_name=tool_name,
                ip_address=ip_address,
                user_agent=user_agent,
                response_time=response_time,
                request_payload=request_payload,
                response_status=response_status,
            )
            db.add(log_entry)
            db.commit()

        return response