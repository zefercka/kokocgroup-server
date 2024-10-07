from typing import Optional
from pydantic import BaseModel
from datetime import date
from ..schemas.role import Role
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    date_of_birth: date
    phone_number: Optional[str] = None


class CreateUser(UserBase):
    password: str
    

class User(UserBase):
    id: int
    roles: list["Role"]

    class Config:
        from_attributes = True
        

class AuthorizedUser(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str
    user: User