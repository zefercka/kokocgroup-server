from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.user import User, AuthorizedUser, CreateUser
from ..schemas.authorization import Authorization
from ..schemas.token import SendToken, Token
from ..dependecies.database import get_db
from ..services import user_service, auth_service

app = APIRouter()

@app.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(db, user_id)
    return user


@app.get("/", response_model=list[User])
async def get_users(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(db, limit, offset)
    return users
    

@app.post("/auth/login", response_model=AuthorizedUser)
async def login(form_data: Authorization, db: AsyncSession = Depends(get_db)):
    return await user_service.authorize_user(db, form_data)
    

@app.post("/auth/register", response_model=AuthorizedUser)
async def register(user: CreateUser, db: AsyncSession = Depends(get_db)):
    return await user_service.register_user(db, user)
    
    
@app.post("/auth/refresh", response_model=SendToken)
async def update_tokens(refresh_token: Token = Depends(auth_service.get_current_token),  db: AsyncSession = Depends(get_db)):
    print(refresh_token.token)
    return await user_service.new_tokens(db, refresh_token)
    
    
@app.delete("/auth/logout")
async def logout(refresh_token: str = Depends(auth_service.get_current_token), db: AsyncSession = Depends(get_db)):
    await user_service.logout_user(db, refresh_token)
    
    
@app.post("/{user_id}/roles/{role_id}")
async def add_role_to_user(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    await user_service.add_role_to_user(db, user_id, role_id)
    

# Delete after
# @app.post("/permission")
# async def add_permission(user_id: int, permission_id: int, db: AsyncSession = Depends(get_db)):
    