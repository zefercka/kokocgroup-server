from pydantic import BaseModel


class Authorization(BaseModel):
    login: str
    password: str
