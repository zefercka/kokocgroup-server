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
    expires_at: datetime | None = None


class SendToken(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str

    
class TokenData(BaseModel):
    user_id: int | None = None
    

class AuthorizedUser(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str
    user: User


class Authorization(BaseModel):
    login: str
    password: str
    
    
class Role(BaseModel):
    id: int | None = None
    name: str
    access_level: int