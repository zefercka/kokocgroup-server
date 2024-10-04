from fastapi import APIRouter, Depends, HTTPException, status
from ..dependecies.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
# from fastapi.security import OAuth2PasswordRequestForm
from ..services import user_service

app = APIRouter()

@app.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(db, user_id)
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


@app.get("/", response_model=list[schemas.User])
async def get_users(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    users = await user_service.get_users(db, limit, offset)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователи не найдены")
    return users


# Доделать ошибки
@app.post("/")
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        await user_service.create_user(db, user)
    except (IntegrityError, ) as err:
        print(err)
        if err.orig is UniqueViolationError:
            print("Pizdec")
    

@app.post("/auth/login")
async def login(form_data: schemas.Authorization, db: AsyncSession = Depends(get_db)) -> schemas.AuthorizedUser:
    try:
        user = await user_service.authorise_user(db, form_data.username, form_data.password)
        return user
    except Exception as err:
        raise err
    


