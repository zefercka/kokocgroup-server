from typing import Optional
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from api.database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[Optional[str]]
    date_of_birth: Mapped[date]
    phone_number: Mapped[Optional[str]]
    avatar_url: Mapped[Optional[str]]
    password_hash: Mapped[str]
    
    