from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Пользователь не найден"
        )

    
class TokenExpired(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Срок действия токена истёк"
        )
    

class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Неверный токен"  
        )  


class UnexpectedTokenType(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Ожидался другой тип токена"
        )
    

class TokenRevoked(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Токен более не действителен"
        )


class RoleNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Роль не найдена"
        )
        

class NoPermissions(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Нет разрешений"
        )