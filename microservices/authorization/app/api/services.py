from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas, dependencies
from fastapi import HTTPException, status, Depends
import jwt
from typing import Annotated
# from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "1d9a7b4577355c1e0c8d31edf503ef4d85e4b3f9f1c96506dde4ebc4a68d2885"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    results = await db.execute(select(models.User).where(models.User.id == user_id))
    return results.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> models.User | None:
    results = await db.execute(select(models.User).where(models.User.username == username))
    return results.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    results = await db.execute(select(models.User).where(models.User.email == email))
    return results.scalars().first()


async def get_users(db: AsyncSession, limit: int = 50, offset: int = 0) -> models.User | None:
    results = await db.execute(select(models.User).order_by(models.User.id).limit(limit).offset(offset))
    return results.scalars().all()


async def create_user(db: AsyncSession, user_create: schemas.UserCreate) -> models.User | None:
    user_data = user_create.dict(exclude={"password"})
    user_data["password_hash"] = await dependencies.get_password_hash(user_create.password)
    user = models.User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, login: str, password: str) -> models.User | None:
    user = await get_user_by_username(db, login) or await get_user_by_email(db, login)
    if user is None:
        return None

    if await dependencies.verify_password(password, user.password_hash):
        return user

    return None


async def get_current_user(db: AsyncSession, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except Exception as err:
        print(err)
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user