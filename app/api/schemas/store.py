from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BaseStoreItem(BaseModel):
    title: str = Field(min_length=4, max_length=128)
    price: int
    description: str
    category_name: str
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
    pass
    
    