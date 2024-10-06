from typing import Optional, List
from sqlalchemy import String, func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, Relationship
from .dependecies.database import Base
from datetime import date, datetime


users_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True)
)


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
    roles: Mapped[List["Role"]] = relationship(
        secondary=users_roles, back_populates="users", lazy="selectin"
    )
    

class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    access_level: Mapped[int]
    
    users: Mapped[List["User"]] = relationship(
        secondary=users_roles, back_populates="roles", lazy="selectin"
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    token: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expire_date: Mapped[datetime]
    
    user: Mapped["User"] = relationship(back_populates="tokens")    
    
    
class News(Base):
    __tablename__ = "news"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    event_date: Mapped[datetime]
    news_date: Mapped[datetime]
    content: Mapped[str]
    category: Mapped[str]
    image_url: Mapped[str] = mapped_column(String(256))