from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: str
    

class User(UserBase):
    id: int

    class Config:
        orm_mode = True