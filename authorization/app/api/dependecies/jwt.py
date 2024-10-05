import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from ..schemas import Token

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
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    token = Token(token=encoded_jwt, token_type="access", expire_date=expire)
    return token


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> Token:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, ALGORITHM)
    token = Token(token=encoded_jwt, token_type="refresh", expire_date=expire)
    return token


async def get_user_id(token: Token) -> int:
    payload = jwt.decode(token.token, settings.ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    print(payload)
    user_id: str = payload.get("sub")
    
    return user_id