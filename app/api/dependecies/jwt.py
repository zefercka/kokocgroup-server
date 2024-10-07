import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from ..schemas.token import Token
import uuid

ALGORITHM = "HS256"
# JWT (подумать куда вынести)
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> Token:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    token = Token(token=encoded_jwt, expires_at=expire)
    return token


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> Token:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    jti = str(uuid.uuid4())
    
    to_encode.update({"exp": expire, "jti": jti, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, ALGORITHM)
    token = Token(token=encoded_jwt, expires_at=expire)
    return token

async def get_payload(token: Token):
    return jwt.decode(token.token, settings.ACCESS_SECRET_KEY, algorithms=[ALGORITHM])


async def get_user_id(token: Token) -> int:
    payload = await get_payload(token)
    user_id = payload.get("sub")
    return user_id


async def get_expire_date(token: Token) -> datetime:
    payload = await get_payload(token)
    expire_date = payload.get("exp")
    return expire_date


async def get_token_type(token: str) -> str:
    payload = await get_payload(token)
    token_type = payload.get("type")
    return token_type

