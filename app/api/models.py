from typing import Optional, List
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .dependecies.database import Base
from datetime import date, datetime


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
    
    tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    # Убрать id и сделать token primary key
    token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expire_date: Mapped[datetime]
    
    user: Mapped["User"] = relationship(back_populates="tokens")