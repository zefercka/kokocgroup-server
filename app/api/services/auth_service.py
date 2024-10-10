from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import text

from ..cruds import refresh_token as token_crud
from ..cruds import user as crud
from ..dependecies import hash, jwt
from ..dependecies.database import get_db
from ..dependecies.exceptions import (InvalidToken, TokenExpired, TokenRevoked,
                                      UnexpectedTokenType, UserNotFound)
from ..schemas.authorization import Authorization
from ..schemas.token import SendToken, Token
from ..schemas.user import AuthorizedUser, CreateUser, SendUser, User
from ..services import user_service

token_key = APIKeyHeader(name="Authorization")


async def authorize_user(db: AsyncSession, data: Authorization) -> AuthorizedUser:
    
    # db.execute(text('CREATE EXTENSION IF NOT EXISTS pg_trgm'))
    
    user = await authenticate_user(db, data.login, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
        
    access_token = await jwt.create_access_token(data={"sub": user.id})
    refresh_token = await jwt.create_refresh_token(data={"sub": user.id})
    
    await token_crud.add_token(
        db, token=refresh_token.token, expired_date=refresh_token.expires_at,
        user_id=user.id
    )
    
    user = SendUser.model_validate(user.model_dump(exclude=["roles"]))
    authorized_user = AuthorizedUser(
        user=user, access_token=access_token.token, 
        expires_at=access_token.expires_at, refresh_token=refresh_token.token
    )
    
    print(authorized_user)
    
    return authorized_user


async def register_user(db: AsyncSession, user_create: CreateUser) -> AuthorizedUser:
    is_unique_user = \
        False if await crud.get_user_by_email(db, user_create.email) or \
        await crud.get_user_by_username(db, user_create.username) else True
    
    if is_unique_user is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином или почтой уже существует",
        )
    
    user = await crud.add_user(db, **user_create.model_dump())
    user = await user_service.add_base_role_to_user(db, user=user)
    
    data = Authorization(login=user_create.email, password=user_create.password)
    user = await authorize_user(db, data)
    
    return user
 

async def authenticate_user(db: AsyncSession, login: str, password: str) -> User | None:
    user = \
        await crud.get_user_by_username(db, username=login) or \
        await crud.get_user_by_email(db, email=login)
    if user is None:
        return None

    if await hash.verify_password(password, user.password_hash):
        return User.model_validate(user)

    return None


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
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обработки токена"
        )
        

async def new_tokens(db: AsyncSession, refresh_token: Token) -> SendToken:
    try:
        user_id = await jwt.get_user_id(refresh_token)
        token = await token_crud.get_token(db, token=refresh_token.token)
        
        if token is None:
            raise TokenRevoked
            
        await token_crud.delete_token_obj(db, token)
            
        access_token = await jwt.create_access_token(data={"sub": user_id})
        refresh_token = await jwt.create_refresh_token(data={"sub": user_id})
        
        await token_crud.add_token(
            db, token=refresh_token.token, 
            expired_date=refresh_token.expires_at, user_id=user_id
        )
        
        token = SendToken(
            access_token=access_token.token, expires_at=access_token.expires_at, 
            refresh_token=refresh_token.token
        )
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


async def get_current_token(auth_key: str = Security(token_key)) -> Token:
    token = auth_key.split()[-1]
    return Token(token=token)


async def get_current_user(db: AsyncSession = Depends(get_db), 
                           token: Token = Depends(get_current_token)) -> User:    
    try:
        
        user_id = await jwt.get_user_id(token=token)            
        user = await crud.get_user_by_id(db, user_id=user_id)
        
        if user is None:
            raise UserNotFound
        
        return User.model_validate(user)
        
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