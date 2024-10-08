from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from ..cruds.role import get_role_by_id
from ..cruds.user import get_user_by_id, get_users
from ..dependecies.exceptions import RoleNotFound, UserNotFound
from ..schemas.user import User

token_key = APIKeyHeader(name="Authorization")


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    return User.model_validate(user)


async def get_all_users(db: AsyncSession, limit: int, offset: int) -> list[User]:
    users = await get_users(db, limit, offset)
    users = [User.model_validate(user) for user in users]
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
    if permission in user.permissions:
        return True

    return False