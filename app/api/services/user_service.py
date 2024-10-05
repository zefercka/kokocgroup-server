from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models, schemas
from fastapi import HTTPException, status, Depends
from typing import Annotated
from jwt import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from ..dependecies import jwt, hash
from datetime import datetime, timezone
from ..dependecies.database import get_db
from jwt.exceptions import ExpiredSignatureError, DecodeError

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth/logout")


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
    key = False if await get_user_by_email(db, user_create.email) or await get_user_by_username(db, user_create.username) else True
    
    if key is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином или почтой уже существует",
        )
    
    user_data = user_create.model_dump(exclude={"password"})
    user_data["password_hash"] = await hash.get_password_hash(user_create.password)
    user = models.User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_token(db: AsyncSession, token: str):
    results = await db.execute(select(models.RefreshToken).where(models.RefreshToken.token == token))
    return results.scalars().first()


async def delete_token(db: AsyncSession, token: schemas.BaseToken):
    token_obj = await get_token(db, token.token)
    if token_obj is not None:
        await db.delete(token_obj)
        await db.commit()


async def add_token(db: AsyncSession, token: schemas.BaseToken, user_id: int, finger_print: str = "defaultfinger"):
    db_token = models.RefreshToken(
        token=token.token, expire_date=token.expire_date.replace(tzinfo=None), user_id=user_id
    )
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token
    

async def authorize_user(db: AsyncSession, data: schemas.Authorization) -> schemas.AuthorizedUser:
    user = await authenticate_user(db, data.login, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = await jwt.create_access_token(data={"sub": user.id})
    refresh_token = await jwt.create_refresh_token(data={"sub": user.id})
    
    await add_token(db, token=refresh_token, user_id=user.id)
    
    authorized_user = schemas.AuthorizedUser(user=user, access_token=access_token, refresh_token=refresh_token)
    return authorized_user
 

async def authenticate_user(db: AsyncSession, login: str, password: str) -> models.User | None:
    user = await get_user_by_username(db, username=login) or await get_user_by_email(email=login)
    if user is None:
        return None

    if await hash.verify_password(password, user.password_hash):
        return user

    return None


# Переделать, что передаётся не стр, а токен 
async def get_current_user(db: AsyncSession = Depends(get_db), token: schemas.BaseToken | None = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user_id = await jwt.get_user_id(token=token)
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except InvalidTokenError as err:
        print(err)
        raise credentials_exception
    
    user = await get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def new_tokens(db: AsyncSession, refresh_token: schemas.BaseToken) -> dict:
    try:
        user_id = await jwt.get_user_id(refresh_token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истёк"
        )
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )
    except InvalidTokenError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обработки токена"
        )
    
    token = await get_token(db, token=refresh_token.token)
    
    print(token)
    
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен более не действителен"
        )
        
    await delete_token(db, refresh_token) 
        
    access_token = await jwt.create_access_token(data={"sub": user_id})
    refresh_token = await jwt.create_refresh_token(data={"sub": user_id})
    
    await add_token(db, refresh_token, user_id)
    
    # Мб сделать схемой
    return {"access_token": access_token, "refresh_token": refresh_token}