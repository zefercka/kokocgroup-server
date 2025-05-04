from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.api.schemas.user import SendUser, User
from app.api.services import auth_service, users_service

app = APIRouter()


# @app.get("/posts", response_model=SendUser)
# async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     user = await users_service.get_user(db, user_id)
#     return user


# @app.get("/{user_id}/posts", response_model=)