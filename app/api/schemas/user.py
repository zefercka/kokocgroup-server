from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from app.api.schemas.role import Role


class UserBase(BaseModel):
    username: str = Field(min_length=4, max_length=64)
    email: str = Field(min_length=4, max_length=256)
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    date_of_birth: date
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None


class CreateUser(UserBase):
    password: str = Field(min_length=8, max_length=64)
    

class User(UserBase):
    id: int
    roles: list[Role]
    permissions: list[str] = []

    class Config:
        from_attributes = True
    
    @field_validator("roles", mode="before")
    def adjust_roles(roles):
        return [Role(id=role.id, name=role.name, permissions=role.permissions) for role in roles]
    
    @model_validator(mode="after")
    def collect_permissions(cls, values):
        roles = values.roles
        if roles:
            permissions = []
            for role in roles:
                permissions.extend(role.permissions)
            values.permissions = list(set(permissions))
        return values


class SendUser(UserBase):
    id: int
    permissions: list[str]
        

class AuthorizedUser(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str
    user: SendUser