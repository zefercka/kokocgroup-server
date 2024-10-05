from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models, schemas
from fastapi import HTTPException, status, Depends
from typing import Annotated
from jwt import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from ..dependecies import jwt, hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


async def get_token_by_token(db: AsyncSession, token: str):
    results = await db.execute(select(models.RefreshToken).where(models.RefreshToken.token == token))
    return results.scalars().first()


async def delete_token(db: AsyncSession, token: schemas.Token):
    token_obj = await get_token_by_token(db, token.token)
    if token_obj is not None:
        await db.delete(token_obj)
        await db.commit()


async def add_token(db: AsyncSession, token: schemas.Token, user_id: int):
    db_token = models.RefreshToken(token=token.token, expire_date=token.expire_date.replace(tzinfo=None), user_id=user_id)
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token


async def check_token(db: AsyncSession, token: schemas.Token) -> models.RefreshToken | None:
    user_id = jwt.get_user_id(token)
    results = await db.execute(select(models.RefreshToken).where(models.RefreshToken.user_id == user_id))
    


async def authorise_user(db: AsyncSession, login: str, password: str) -> schemas.AuthorizedUser:
    user = await authenticate_user(db, login, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = await jwt.create_access_token(data={"sub": user.id})
    refresh_token = await jwt.create_refresh_token(data={"sub": user.id})
    
    await add_token(db, refresh_token, user.id)
    
    authorized_user = schemas.AuthorizedUser(user=user, access_token=access_token, refresh_token=refresh_token)
    return authorized_user
 

async def authenticate_user(db: AsyncSession, login: str, password: str) -> models.User | None:
    user = await get_user_by_username(db, login) or await get_user_by_email(db, login)
    if user is None:
        return None

    if await hash.verify_password(password, user.password_hash):
        return user

    return None


# Переделать, что передаётся не стр, а токен 
async def get_current_user(db: AsyncSession, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user_id = jwt.get_user_id(token=token)
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except InvalidTokenError as err:
        print(err)
        raise credentials_exception
    
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def new_tokens(db: AsyncSession, refresh_token: schemas.Token) -> dict:
    # check if token is valid
    
    
    user_id = await jwt.get_user_id(refresh_token)
    
    access_token = await jwt.create_access_token(data={"sub": user_id})
    refresh_token_new = await jwt.create_refresh_token(data={"sub": user_id})
    
    await delete_token(db, refresh_token)
    await add_token(db, refresh_token_new, user_id)
    
    return {"access": access_token, "refresh": refresh_token_new}