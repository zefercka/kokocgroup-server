from typing import Optional, List
from sqlalchemy import String, func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .dependecies.database import Base, BaseClear
from datetime import date, datetime


users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True)
)

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission", ForeignKey("permissions.name"), primary_key=True)
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
        secondary="users_roles", back_populates="users", lazy="selectin"
    )

    async def get_permissions(roles):
        permissions = [role.permissions for role in roles]
        return [permission.name for permission in permissions]
    

class Role(BaseClear):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    
    users: Mapped[List["User"]] = relationship(
        secondary="users_roles", back_populates="roles", lazy="selectin"
    )
    
    permissions: Mapped[List["Permission"]] = relationship(
        secondary="roles_permissions", back_populates="roles", lazy="joined"
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
    news_date: Mapped[datetime]
    content: Mapped[str]
    category: Mapped[str]
    image_url: Mapped[str] = mapped_column(String(256))
    
    news_actions: Mapped["NewsAction"] = relationship(
        back_populates="news", cascade="all, delete-orphan"
    )
    

class NewsAction(Base):
    __tablename__ = "news_actions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id"))
    # "create", "edit"
    type: Mapped[str] = mapped_column(String(8))
    
    news: Mapped["News"] = relationship(back_populates="news_actions")
    

class Permission(BaseClear):
    __tablename__ = "permissions"
    
    name: Mapped[str] = mapped_column(String(256), primary_key=True)
    
    roles: Mapped[List["Role"]] = relationship(
        secondary="roles_permissions", back_populates="permissions", lazy="selectin"
    )

    