import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from ..schemas import SendToken, BaseToken

ALGORITHM = "HS256"
# JWT (подумать куда вынести)
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> SendToken:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    token = SendToken(token=encoded_jwt, expire_date=expire)
    return token


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None, finger_print: str = "default_finger") -> SendToken:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "finger_print": finger_print, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, ALGORITHM)
    token = SendToken(token=encoded_jwt, expire_date=expire)
    return token


async def get_user_id(token: BaseToken) -> int:
    payload = jwt.decode(token.token, settings.ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get("sub")
    return user_id


async def get_expire_date(token: BaseToken) -> datetime:
    payload = jwt.decode(token.token, settings.ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    expire_date = payload.get("exp")
    return expire_date


async def check_token_expiration(token: BaseToken) -> bool:
    # Возвращает True, если токен истёк
    expire_date = await get_expire_date(token=token)
    print()
    return datetime.fromtimestamp(expire_date, tz=timezone.utc) <= datetime.now(timezone.utc)