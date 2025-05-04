from pydantic import BaseModel, field_validator

class BaseRole(BaseModel):
    name: str


class CreateRole(BaseRole):
    permissions: list[str]
    

class Role(BaseRole):
    id: int
    permissions: list[str]
    
    class config:
        from_attributes = True
        
    @field_validator("permissions", mode="before")
    def adjust_permissions(permissions):
        if len(permissions) == 0:
            return []

        if type(permissions[0]) == str:
            return permissions
        
        return [permission.name for permission in permissions]
        
    