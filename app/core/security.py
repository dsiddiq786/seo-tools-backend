import bcrypt
import jwt
from datetime import datetime, timedelta
from app.core.config import settings
import os
import re
import subprocess
from passlib.context import CryptContext

# Secure Secret Key (Rotate periodically)
SECRET_KEY = "supersecurelongkeyhere"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expires in 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Refresh Token expires in 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Hash Passwords Securely
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Verify Passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Create Access Token
def create_jwt(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Create Refresh Token
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Decode JWT Token
def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    
def get_mac_address(ip_address):
    """ Get MAC address of the user based on their IP """
    try:
        result = subprocess.check_output(["arp", "-n", ip_address])
        mac = re.search(r"(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})", result.decode())
        return mac.group(0) if mac else "Unknown"
    except Exception:
        return "Unknown"
