from pydantic import BaseModel


class BaseLocation(BaseModel):
    name: str
    address: str

    class Config:
        from_attributes = True


class Location(BaseLocation):
    id: int
    

class CreateLocation(BaseLocation):
    pass
