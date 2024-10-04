from .database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import jwt
# from jwt.exceptions import InvalidTokenError
from fastapi import status
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from typing import Annotated

SECRET_KEY = "1d9a7b4577355c1e0c8d31edf503ef4d85e4b3f9f1c96506dde4ebc4a68d2885"
ALGORITHM = "HS256"
# 30 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
        

async def get_password_hash(password):
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
