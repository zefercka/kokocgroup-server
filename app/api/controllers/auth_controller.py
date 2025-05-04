from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.schemas.authorization import Authorization
from app.api.schemas.token import SendToken, Token
from app.api.schemas.user import AuthorizedUser, CreateUser
from app.api.services import auth_service

app = APIRouter()


@app.post("/login", response_model=AuthorizedUser)
async def login(form_data: Authorization, db: AsyncSession = Depends(get_db)):
    return await auth_service.authorize_user(db, form_data)
    

@app.post("/register", response_model=AuthorizedUser)
async def register(user: CreateUser, db: AsyncSession = Depends(get_db)):
    return await auth_service.register_user(db, user)
    
    
@app.post("/refresh", response_model=SendToken)
async def update_tokens(refresh_token: Token = Depends(auth_service.get_current_token),  db: AsyncSession = Depends(get_db)):
    return await auth_service.new_tokens(db, refresh_token)
    
    
@app.delete("/logout")
async def logout(refresh_token: str = Depends(auth_service.get_current_token), db: AsyncSession = Depends(get_db)):
    await auth_service.logout_user(db, refresh_token)