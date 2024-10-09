from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import transactions

from ..cruds import role as role_crud
from ..cruds import user as crud
from ..dependecies.exceptions import NoPermissions, RoleNotFound, UserNotFound
from ..schemas.user import User

token_key = APIKeyHeader(name="Authorization")


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await crud.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    return User.model_validate(user)


async def get_all_users(db: AsyncSession, limit: int, offset: int) -> list[User]:
    users = await crud.get_users(db, limit, offset)
    users = [User.model_validate(user) for user in users]
    return users

        
async def add_role_to_user(db: AsyncSession, user_id: int, role_id: int) -> User:
    user = await crud.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    role = await role_crud.get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    if role in user.roles:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, 
            detail="User already has this role"
        )
    
    user = await crud.add_role_to_user(db, user=user, role=role)
    return User.model_validate(user)
        

async def remove_role_user(db: AsyncSession, current_user: User, user_id: int, 
                           role_id: int) -> User:
    if not await check_user_permission(current_user, transactions.REMOVE_ROLE):
        raise NoPermissions
    
    user = await crud.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound

    role = await role_crud.get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    if role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, 
            detail="Users does not have this role"
        )
        
    user = await crud.remove_role_user(db, user=user, role=role)
    
    return User.model_validate(user)


async def check_user_permission(user: User, permission: str) -> bool:    
    if permission in user.permissions:
        return True

    return False