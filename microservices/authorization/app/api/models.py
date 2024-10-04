from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from api.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256))
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]
    avatar_url: Mapped[Optional[str]]
    password_hash: Mapped[str]