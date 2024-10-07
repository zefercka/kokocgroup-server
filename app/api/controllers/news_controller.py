from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.news import CreateNews, News
from ..schemas.user import User
from ..dependecies.database import get_db
from ..services import news_service, auth_service

app = APIRouter()


@app.get("/{news_id}", response_model=News)
async def get_news(news_id: int, db: AsyncSession = Depends(get_db)):
    news = await news_service.get_news(db, news_id)
    return news


@app.get("/", response_model=list[News])
async def get_all_news(limit: int = 10, offset: int = 0, db: AsyncSession = Depends(get_db)):
    news = await news_service.get_all_news(db, limit, offset)
    return news


@app.post("/", response_model=News)
async def create_news(news: CreateNews, current_user: User = Depends(auth_service.get_current_user), db: AsyncSession = Depends(get_db)):
    news = await news_service.create_news(db, news, current_user=current_user)
    return news

