from asyncio import Lock

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from ..cruds import news, refresh_token
from ..dependecies.database import SessionLocal

lock = Lock()

scheduled_cleaner = AsyncIOScheduler()


@logger.catch
@scheduled_cleaner.scheduled_job("cron", hour=0, minute=0)
async def clean_tokens():
    async with lock:
        async with SessionLocal() as db:
            try:
                logger.info("Starting to delete expired tokens...")
                await refresh_token.delete_expired_tokens(db)
            finally:
                await db.close()
                logger.info("Expired tokens successful deleted.")


@logger.catch
@scheduled_cleaner.scheduled_job("cron", hour=0, minute=0)
async def clean_news():
    async with lock:
        async with SessionLocal() as db:
            try:
                logger.info("Starting to delete expired news...")
                await news.delete_expired_news(db)
            finally:
                await db.close()
                logger.info("Expired news successful deleted.")