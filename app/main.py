from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.controllers.auth_controller import app as auth_controller
from .api.controllers.events_controller import app as events_controller
from .api.controllers.files_controller import app as files_controller
from .api.controllers.locations_controller import app as locations_controller
from .api.controllers.members_controller import app as members_controller
from .api.controllers.news_controller import app as news_controller
from .api.controllers.roles_controller import app as role_controller
from .api.controllers.store_controller import app as store_controller
from .api.controllers.teams_controller import app as teams_controller
from .api.controllers.users_controller import app as user_controller

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
app.include_router(files_controller, prefix="/api/v1/files", tags=["Files"])
app.include_router(teams_controller, prefix="/api/v1/teams", tags=["Teams"])
app.include_router(members_controller, prefix="/api/v1/teams/kokoc/members", tags=["Team members"])
app.include_router(events_controller, prefix="/api/v1/events", tags=["Events"])
app.include_router(locations_controller, prefix="/api/v1/locations", tags=["Locations"])
app.include_router(store_controller, prefix="/api/v1/store", tags=["Store"])