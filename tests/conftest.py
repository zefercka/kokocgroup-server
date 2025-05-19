import asyncio
import os
from datetime import datetime
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.api.models import Base
from app.api.dependencies.database import SQLALCHEMY_DATABASE_URL

DATA_DUMP_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/test_data.sql"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        if os.path.exists(DATA_DUMP_FILE):
            with open(DATA_DUMP_FILE, "r") as f:
                sql = f.readlines()
            for i in sql:
                await conn.execute(text(i))

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    


@pytest_asyncio.fixture(scope="function")
async def session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with session_maker() as db:
        yield db