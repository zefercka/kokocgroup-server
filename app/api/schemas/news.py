from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class BaseNews(BaseModel):
    title: str
    news_date: datetime
    content: str
    category_name: str
    image_url: Optional[str] = "url"
    

class CreateNews(BaseNews):
    pass


class News(BaseNews):
    id: int
    
    class Config:
        from_attributes = True