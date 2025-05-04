import re

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cruds import refresh_token as token_crud
from app.api.cruds import user as crud
from app.api.dependencies import hash, jwt
from app.api.dependencies.database import get_db
from app.api.dependencies.exceptions import (InternalServerError, InvalidEmail,
                                             InvalidToken, TokenExpired,
                                             TokenRevoked, UnexpectedTokenType,
                                             UserNotFound)
from app.api.schemas.authorization import Authorization
from app.api.schemas.token import SendToken, Token
from app.api.schemas.user import AuthorizedUser, CreateUser, SendUser, User
from app.api.services import users_service
from app.logger import logger

token_key = APIKeyHeader(name="Authorization")

async def authorize_user(db: AsyncSession, data: Authorization) -> AuthorizedUser:
    user = await authenticate_user(db, data.login, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
        
    try:
        access_token, refresh_token = await jwt.issue_tokens_for_user(db, user_id=user.id)

        user = SendUser.model_validate(user.model_dump(exclude=["roles"]))
        authorized_user = AuthorizedUser(
            user=user,
            access_token=access_token.token,
            expires_at=access_token.expires_at,
            refresh_token=refresh_token.token
        )
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
    
    return authorized_user


async def register_user(db: AsyncSession, user_create: CreateUser) -> AuthorizedUser:
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", user_create.email):
        raise InvalidEmail
    
    try:
        is_unique_user = \
            False if await crud.get_user_by_email(db, user_create.email) or \
            await crud.get_user_by_username(db, user_create.username) else True
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
    
    if is_unique_user is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином или почтой уже существует",
        )
    
    try:
        user = await crud.add_user(db, **user_create.model_dump())
        user = await users_service.add_base_role_to_user(db, user=user)
        
        data = Authorization(login=user_create.email, password=user_create.password)
        user = await authorize_user(db, data)
        
        return user
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
 

async def authenticate_user(db: AsyncSession, login: str, 
                            password: str) -> User | None:
    
    try:
        user = \
            await crud.get_user_by_username(db, username=login) or \
            await crud.get_user_by_email(db, email=login)
        if user is None:
            return None

        if await hash.verify_password(password, user.password_hash):
            return User.model_validate(user)
        
        return None
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError


async def logout_user(db: AsyncSession, token: Token):    
    try:
        token_type = await jwt.get_token_type(token=token)
        
        if token_type != "refresh":
            raise UnexpectedTokenType
        
        token_obj = await token_crud.get_token(db, token.token)
        if token_obj is None:
            raise TokenRevoked
        await token_crud.delete_token_obj(db, token_obj)
    except ExpiredSignatureError:
        raise TokenExpired
    except DecodeError:
        raise InvalidToken
    except InvalidTokenError as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
        

async def refresh_tokens_by_refresh_token(
    db: AsyncSession, refresh_token: Token
) -> SendToken:
    try:        
        user_id = jwt.get_user_id(refresh_token)
        stored_token = await token_crud.get_token(db, token=refresh_token.token)
        
        if stored_token is None:
            raise TokenRevoked
            
        await token_crud.delete_token_obj(db, token)
            
        access_token, refresh_token = await jwt.issue_tokens_for_user(
            db, user_id=user_id
        )
        
        token = SendToken(
            access_token=access_token.token,
            expires_at=access_token.expires_at,
            refresh_token=refresh_token.token
        )
        return token
    except ExpiredSignatureError:
        raise TokenExpired
    except DecodeError:
        raise InvalidToken
    except InvalidTokenError as err:
        logger.error(err, exc_info=True)
        raise InternalServerError


async def get_current_token(auth_key: str = Security(token_key)) -> Token:
    if not auth_key or not auth_key.startswith("Bearer "):
        raise InvalidToken
    
    token = auth_key.removeprefix("Bearer ").strip()
    return Token(token=token)


async def get_current_user(db: AsyncSession = Depends(get_db), 
                           token: Token = Depends(get_current_token)) -> User:    
    try:
        token_type = jwt.get_token_type(token=token)
        if token_type != "access":
            raise UnexpectedTokenType
        
        user_id = jwt.get_user_id(token=token)            
        user = crud.get_user_by_id(db, user_id=user_id)
        
        if user is None:
            raise UserNotFound
        
        return User.model_validate(user)
        
    except ExpiredSignatureError:
        raise TokenExpired
    except DecodeError:
        raise InvalidToken
    except InvalidTokenError as err:
        logger.error(err, exc_info=True)
        raise InternalServerError