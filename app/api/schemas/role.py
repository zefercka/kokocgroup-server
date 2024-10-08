from pydantic import BaseModel, field_validator


class BaseRole(BaseModel):
    name: str


class CreateRole(BaseRole):
    transactions: list[str]
    

class Role(BaseRole):
    id: int
    permissions: list[str]
    
    class config:
        from_attributes = True
        
    @field_validator("permissions", mode="before")
    def adjust_permissions(permissions):
        return [permission.name.lower() for permission in permissions]
        
    