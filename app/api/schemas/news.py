from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class BaseNews(BaseModel):
    title: str
    news_date: datetime
    content: str
    category: str
    image_url: Optional[str] = "url"
    

class CreateNews(BaseModel):
    pass


class News(BaseModel):
    id: int
    
    class Config:
        from_attributes = True