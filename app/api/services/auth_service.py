from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..cruds.user import get_user_by_id
from ..dependecies import jwt

from ..dependecies.exceptions import InvalidToken, TokenExpired, UserNotFound
from ..dependecies.database import get_db

token_key = APIKeyHeader(name="Authorization")


async def get_current_token(auth_key: str = Security(token_key)) -> schemas.Token:
    token = auth_key.split()[-1]
    return schemas.Token(token=token)


async def get_current_user(db: AsyncSession = Depends(get_db), token: schemas.Token = Depends(get_current_token)) -> schemas.User:    
    try:
        user_id = await jwt.get_user_id(token=token)            
        user = await get_user_by_id(db, user_id=user_id)
        
        if user is None:
            raise UserNotFound
        
        return user
        
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