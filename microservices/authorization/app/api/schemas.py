from typing import Optional
from pydantic import BaseModel
from datetime import date


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
        

class AuthorizedUser(BaseModel):
    access_token: str
    refresh_token: str
    user: User



class Authorization(BaseModel):
    username: str
    password: str
        

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    username: str | None = None