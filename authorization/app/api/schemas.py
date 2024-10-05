from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    date_of_birth: date
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: str
    

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        
        
class Token(BaseModel):
    token: str
    token_type: str
    expire_date: datetime
    
    
class TokenData(BaseModel):
    user_id: str | None = None
    

class AuthorizedUser(BaseModel):
    access_token: Token
    refresh_token: Token
    user: User



class Authorization(BaseModel):
    login: str
    password: str