from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
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
    
    # @field_validator("permissions", "roles", mode="after")
    # def adjust_permissions(roles):
    #     permissions = []
    #     for role in roles:
    #         permissions.extend(role.permissions)
    #     print(permissions)
    #     return list(set(permissions))
        

class AuthorizedUser(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str
    user: User