from fastapi import Header, APIRouter, Depends, HTTPException, status
from .dependencies import get_db, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, models
from . import services
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

app = APIRouter()

@app.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await services.get_user(db, user_id)
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User wasn't found")
    return user


@app.get("/", response_model=list[schemas.User])
async def get_users(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    users = await services.get_users(db, limit, offset)
    if users is None:
        raise HTTPException(status_code=404, detail="Users weren't found")
    return users


# Доделать ошибки
@app.post("/")
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        await services.create_user(db, user)
    except (IntegrityError, ) as err:
        print(err)
        if err.orig is UniqueViolationError:
            print("Pizdec")
    

@app.post("/auth")
async def login(form_data: schemas.AuthUser, db: AsyncSession = Depends(get_db)) -> schemas.User:
    print(form_data)
    user = await services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # return Token(access_token=access_token, token_type="bearer")
    return user