from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .dependecies.database import Base, BaseClear

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="NO ACTION", onupdate="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
)

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("permission", ForeignKey("permissions.name", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
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
    category_name: Mapped[str] = mapped_column(ForeignKey("news_categories.name", ondelete="SET NULL", onupdate="CASCADE"))
    image_url: Mapped[str] = mapped_column(String(256))
    
    news_actions: Mapped["NewsAction"] = relationship(
        back_populates="news", cascade="all, delete-orphan"
    )
    category: Mapped["NewsCategory"] = relationship(
        back_populates="news"
    )
    

class NewsAction(Base):
    __tablename__ = "news_actions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="NO ACTION", onupdate="CASCADE"))
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id", ondelete="NO ACTION", onupdate="CASCADE"))
    # "create", "edit"
    type: Mapped[str] = mapped_column(String(8))
    
    news: Mapped["News"] = relationship(
        back_populates="news_actions"
    )
    

class Permission(BaseClear):
    __tablename__ = "permissions"
    
    name: Mapped[str] = mapped_column(String(256), primary_key=True)
    
    roles: Mapped[List["Role"]] = relationship(
        secondary="roles_permissions", back_populates="permissions", lazy="selectin"
    )


class NewsCategory(BaseClear):
    __tablename__ = "news_categories"
    
    name: Mapped[str] = mapped_column(String(32), primary_key=True)
    
    news: Mapped["News"] = relationship(
        back_populates="category"
    )
    

class FileUpload(Base):
    __tablename__ = "file_uploads"
    
    file_name: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] =  mapped_column(ForeignKey("users.id", ondelete="NO ACTION", onupdate="CASCADE"))