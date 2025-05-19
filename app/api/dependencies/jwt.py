import uuid
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cruds import refresh_token as token_crud
from app.api.dependencies.exceptions import InvalidToken, UnexpectedTokenType
from app.api.schemas.token import AccessToken, RefreshToken, Token
from app.config import settings

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
    token = AccessToken(token=encoded_jwt, expires_at=expire)
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
    token = RefreshToken(token=encoded_jwt, expires_at=expire)
    return token

def _get_secret_key_from_token_type(token: Token) -> str:
    try:
        token_str = token.token
        unverified_payload = jwt.decode(
            token_str, options={"verify_signature": False}
        )
        token_type = unverified_payload.get("type")
    except Exception:
        raise InvalidToken
    
    if token_type == "access":
        return settings.ACCESS_SECRET_KEY
    elif token_type == "refresh":
        return settings.REFRESH_SECRET_KEY
    else:
        raise UnexpectedTokenType

def get_payload(token: Token) -> dict:
    key = _get_secret_key_from_token_type(token)
    return jwt.decode(token.token, key=key, algorithms=[ALGORITHM])



def get_user_id(token: Token) -> int:
    payload = get_payload(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidToken
    return int(user_id)


def get_expire_date(token: Token) -> datetime:
    payload = get_payload(token)
    expire_timestamp = payload.get("exp")
    if expire_timestamp is None:
        raise InvalidToken
    return datetime.fromtimestamp(expire_timestamp, tz=timezone.utc)


def get_token_type(token: Token) -> str:
    payload = get_payload(token)
    token_type = payload.get("type")
    return token_type


async def issue_tokens_for_user(db: AsyncSession, user_id: int) -> tuple[AccessToken, RefreshToken]:
    access_token = await create_access_token(data={"sub": str(user_id)})
    refresh_token = await create_refresh_token(data={"sub": str(user_id)})

    await token_crud.add_token(
        db=db,
        token=refresh_token.token,
        expired_date=refresh_token.expires_at,
        user_id=user_id
    )

    return access_token, refresh_token