from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

SECRET = os.environ["JWT_SECRET"]          # new env var, see below
ALG    = "HS256"
ACCESS_TTL  = timedelta(hours=1)
REFRESH_TTL = timedelta(days=14)

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd.verify(plain, hashed)

def create_access_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + ACCESS_TTL,
        "type": "access",
    }
    return jwt.encode(payload, SECRET, algorithm=ALG)

def create_refresh_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + REFRESH_TTL,
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET, algorithm=ALG)

def decode_token(token: str) -> dict:
    """Raises JWTError on bad/expired token."""
    return jwt.decode(token, SECRET, algorithms=[ALG])