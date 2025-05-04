from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import models
from app.api.cruds import role as r_crud
from app.api.cruds import settings as settings_crud
from app.api.cruds import user as crud
from app.api.dependencies.exceptions import (NoPermissions, RoleNotFound,
                                             UserNotFound)
from app.api.schemas.user import User
from app.config import db_constants, transactions

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

        
async def add_role_to_user(db: AsyncSession, user_id: int, role_id: int,
                           current_user: User) -> User:
    await check_user_permission(current_user, transactions.ADD_ROLE)
    
    user = await crud.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    role = await r_crud.get_role_by_id(db, role_id=role_id)
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
    await check_user_permission(current_user, transactions.REMOVE_ROLE)
    
    user = await crud.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound

    role = await r_crud.get_role_by_id(db, role_id=role_id)
    
    if role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, 
            detail="Пользователь уже имеет эту роль"
        )
        
    user = await crud.remove_role_user(db, user=user, role=role)
    
    return User.model_validate(user)


async def check_user_permission(user: User, permission: str):    
    if permission not in user.permissions:
        raise NoPermissions


async def add_base_role_to_user(db: AsyncSession, user: models.User):
    base_role_id = await settings_crud.get_settings(
        db, db_constants.BASE_ROLE
    )
    if base_role_id is not None:
        base_role_id = int(base_role_id.value)
        base_role = await r_crud.get_role_by_id(db, role_id=base_role_id)
        if base_role is not None:
            user = await crud.add_role_to_user(db, user, base_role)