from pydantic import BaseModel


class BaseRole(BaseModel):
    name: str


class CreateRole(BaseRole):
    transactions: list[str]
    

class Role(BaseRole):
    id: int
    
    class config:
        from_attributes = True