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

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


@app.get("/", response_model=list[schemas.User])
async def get_users(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    users = await user_service.get_users(db, limit, offset)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователи не найдены")
    return users
    

@app.post("/auth/login", response_model=schemas.AuthorizedUser)
async def login(form_data: schemas.Authorization, db: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.authorise_user(db, form_data.login, form_data.password)
        return user
    except Exception as err:
        raise err
    

@app.post("/auth/register", response_model=schemas.AuthorizedUser)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await user_service.create_user(db, user)
        return await user_service.authorise_user(db, db_user.email, user.password)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@app.post("/auth/refresh", response_model=dict)
async def update_tokens(refresh_token: schemas.Token, db: AsyncSession = Depends(get_db)):
    return await user_service.new_tokens(db, refresh_token)
    
# @app.post("/auth/logout")
# async def logout(user: schemas):
#     return 0
    


