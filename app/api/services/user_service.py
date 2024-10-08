from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from ..schemas.user import User
from ..schemas.role import Role
from ..cruds.user import get_user_by_id, get_users
from ..cruds.role import get_role_by_id

from ..dependecies.exceptions import UserNotFound, RoleNotFound

token_key = APIKeyHeader(name="Authorization")


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    return User.model_validate(user)


async def get_all_users(db: AsyncSession, limit: int, offset: int) -> list[models.User]:
    users = await get_users(db, limit, offset)
    return users

        
async def add_role_to_user(db: AsyncSession, user_id: int, role_id: int):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    role = await get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    user.roles.append(role)
    await db.commit()
        

async def check_user_permission(user: User, permission: str) -> bool:    
    for role in user.roles:
        if permission in role.permissions:
            return True

    return False