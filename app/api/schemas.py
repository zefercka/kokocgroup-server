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
        
        
class BaseToken(BaseModel):
    token: str

        
class SendToken(BaseToken):
    expire_date: datetime
    
    
class TokenData(BaseModel):
    user_id: int | None = None
    

class AuthorizedUser(BaseModel):
    access_token: SendToken
    refresh_token: SendToken
    user: User



class Authorization(BaseModel):
    login: str
    password: str