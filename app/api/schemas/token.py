from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token: str
    expires_at: Optional[datetime] = None


class SendToken(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str


class TokenData(BaseModel):
    user_id: int | None = None