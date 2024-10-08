from typing import Optional
from pydantic import BaseModel, field_validator
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
    roles: list[Role]

    class Config:
        from_attributes = True
    
    @field_validator("roles", mode="before")
    def adjust_roles(roles):
        return [Role(id=role.id, name=role.name, permissions=role.permissions) for role in roles]
        

class AuthorizedUser(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str
    user: User