from fastapi import FastAPI

from api.routers import auth

app = FastAPI()

app.include_router(auth, prefix='/api/v1/users', tags=['users'])