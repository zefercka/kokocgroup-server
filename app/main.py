from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.controllers.user_controller import app as user_controller
from .api.controllers.auth_controller import app as auth_controller
from .api.controllers.role_controller import app as role_controller
from .api.controllers.news_controller import app as news_controller

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

app.include_router(user_controller, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth_controller, prefix="/api/v1/users/auth", tags=["Authorization"])
app.include_router(role_controller, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(news_controller, prefix="/api/v1/news", tags=["News"])