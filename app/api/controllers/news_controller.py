from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.news import CreateNews, News
from ..schemas.user import User
from ..dependecies.database import get_db
from ..services import news_service, auth_service

app = APIRouter()


@app.get("/categories", response_model=list[str])
async def get_news_categories(db: AsyncSession = Depends(get_db)):
    categories = await news_service.get_all_categories(db)
    return categories


@app.get("/", response_model=list[News])
async def get_all_news(limit: int = 10, offset: int = 0, db: AsyncSession = Depends(get_db)):
    news = await news_service.get_all_news(db, limit, offset)
    return news


@app.get("/{news_id}", response_model=News)
async def get_news(news_id: int, db: AsyncSession = Depends(get_db)):
    news = await news_service.get_news(db, news_id)
    return news


@app.delete("/{news_id}")
async def delete_news(news_id: int, current_user: User = Depends(auth_service.get_current_user), 
                      db: AsyncSession = Depends(get_db)):
    await news_service.delete_news(db, news_id=news_id, current_user=current_user)


@app.put("/", response_model=News)
async def update_news(news: News, current_user: User = Depends(auth_service.get_current_user), 
                      db: AsyncSession = Depends(get_db)):
    news = await news_service.update_news(db, news, current_user=current_user)
    return news


@app.post("/", response_model=News)
async def create_news(news: CreateNews, current_user: User = Depends(auth_service.get_current_user), 
                      db: AsyncSession = Depends(get_db)):
    news = await news_service.create_news(db, news, current_user=current_user)
    return news