from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import app as user_route
from api.database import engine, Base

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route, prefix='/api/v1/users', tags=['users'])