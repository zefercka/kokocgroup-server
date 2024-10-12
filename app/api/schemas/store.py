from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class Males(Enum):
    MALE = "муж"
    FEMALE = "жен"
    UNI = "муж/жен"


class BaseStoreItem(BaseModel):
    title: str
    price: int
    description: str
    category_name: str
    male: Males
    image_url: str
    sizes: Optional[list[str]] = []
    
    class Config:
        from_attributes = True
        
    @field_validator("sizes", mode="before")
    def adjust_sizes(sizes):
        if len(sizes) == 0:
            return []
        
        if type(sizes[0]) == str:
            return sizes
        
        return [size.size for size in sizes]


class StoreItem(BaseStoreItem):
    id: int
    
    
class CreateStoreItem(BaseStoreItem):
    
    
    