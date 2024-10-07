from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..cruds.refresh_token import add_token, delete_token_obj, get_token
from ..cruds.user import get_user_by_id, get_user_by_email, get_user_by_username, add_user
from ..cruds.role import get_role_by_id
from ..cruds.permission import get_permission
from ..dependecies import hash, jwt

from ..dependecies.exceptions import InvalidToken, TokenExpired, TokenRevoked, UnexpectedTokenType, UserNotFound, RoleNotFound

token_key = APIKeyHeader(name="Authorization")


async def get_user(db: AsyncSession, user_id: int) -> models.User:
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    return user


async def get_users(db: AsyncSession, limit: int, offset: int) -> list[models.User]:
    users = await get_users(db, limit, offset)
    return users


async def register_user(db: AsyncSession, user_create: schemas.UserCreate) -> schemas.AuthorizedUser:
    is_unique_user = False if await get_user_by_email(db, user_create.email) or await get_user_by_username(db, user_create.username) else True
    
    if is_unique_user is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином или почтой уже существует",
        )
    
    await add_user(db, **user_create.model_dump())
    
    data = schemas.Authorization(login=user_create.email, password=user_create.password)
    user = await authorize_user(db, data)
    
    return user

        
async def add_role_to_user(db: AsyncSession, user_id: int, role_id: int):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound
    
    role = await get_role_by_id(db, role_id)
    if role is None:
        raise RoleNotFound
    
    user.roles.append(role)
    await db.commit()
    

async def authorize_user(db: AsyncSession, data: schemas.Authorization) -> schemas.AuthorizedUser:
    user = await authenticate_user(db, data.login, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
        
    access_token = await jwt.create_access_token(data={"sub": user.id})
    refresh_token = await jwt.create_refresh_token(data={"sub": user.id})
    
    await add_token(
        db, token=refresh_token.token, expired_date=refresh_token.expires_at, user_id=user.id
    )
    
    authorized_user = schemas.AuthorizedUser(
        user=user, access_token=access_token.token, expires_at=access_token.expires_at, refresh_token=refresh_token.token
    )
    
    print(authorized_user)
    
    return authorized_user
 

async def authenticate_user(db: AsyncSession, login: str, password: str) -> schemas.User | None:
    user = await get_user_by_username(db, username=login) or await get_user_by_email(db, email=login)
    if user is None:
        return None

    if await hash.verify_password(password, user.password_hash):
        return schemas.User.model_validate(user)

    return None


async def logout_user(db: AsyncSession, token: schemas.Token):    
    try:
        token_type = await jwt.get_token_type(token=token)
        
        if token_type != "refresh":
            raise UnexpectedTokenType
        
        token_obj = await get_token(db, token.token)
        if token_obj is None:
            raise TokenRevoked
        await delete_token_obj(db, token_obj)
    except ExpiredSignatureError:
        raise TokenExpired
    except DecodeError:
        raise InvalidToken
    except InvalidTokenError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обработки токена"
        )
        

async def new_tokens(db: AsyncSession, refresh_token: schemas.Token) -> schemas.SendToken:
    try:
        user_id = await jwt.get_user_id(refresh_token)
        token = await get_token(db, token=refresh_token.token)
        
        if token is None:
            raise TokenRevoked
            
        await delete_token_obj(db, token)
            
        access_token = await jwt.create_access_token(data={"sub": user_id})
        refresh_token = await jwt.create_refresh_token(data={"sub": user_id})
        
        await add_token(db, token=refresh_token.token, expired_date=refresh_token.expires_at, user_id=user_id)
        
        token = schemas.SendToken(
            access_token=access_token.token, expires_at=access_token.expires_at, refresh_token=refresh_token.token
        )
        print(token)
        return token
        
    except ExpiredSignatureError:
        raise TokenExpired
    except DecodeError:
        raise InvalidToken
    except InvalidTokenError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обработки токена"
        )
        

async def check_user_permission(db: AsyncSession, user: models.User, permission: str) -> bool:
    permission = await get_permission(db, permission=permission)
    
    if any(role in permission.roles for role in user.roles):
        return True
    return False