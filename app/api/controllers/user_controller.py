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
        
    
@app.post("/{user_id}/roles/{role_id}")
async def add_role_to_user(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    await user_service.add_role_to_user(db, user_id, role_id)
    

# Delete after
# @app.post("/permission")
# async def add_permission(user_id: int, permission_id: int, db: AsyncSession = Depends(get_db)):
    