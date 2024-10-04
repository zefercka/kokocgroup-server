from fastapi import FastAPI

from api.routers import app as user_route
from api.database import engine, Base

app = FastAPI()

app.include_router(user_route, prefix='/api/v1/users', tags=['users'])