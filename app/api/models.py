from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, String, Table, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import db_constants

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
    

class Role(BaseClear):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    
    users: Mapped[List["User"]] = relationship(
        secondary="users_roles", back_populates="roles", lazy="selectin"
    )
    
    permissions: Mapped[List["Permission"]] = relationship(
        secondary="roles_permissions", back_populates="roles", lazy="selectin"
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
    title: Mapped[str] = mapped_column(String(256))
    news_date: Mapped[datetime]
    content: Mapped[str] = mapped_column(String)
    category_name: Mapped[str] = mapped_column(ForeignKey("news_categories.name", ondelete="SET NULL", onupdate="CASCADE"))
    image_url: Mapped[str] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(default=db_constants.NEWS_AVAILABLE)
    
    news_actions: Mapped["NewsAction"] = relationship(
        back_populates="news", cascade="all, delete-orphan"
    )
    category: Mapped["NewsCategory"] = relationship(
        back_populates="news"
    )
    
    __table_args__ = (
        Index('ix_title_content', 
              func.coalesce(title, '').concat(
                  func.coalesce(content, '')).label('news_search'),
              postgresql_using='gin', 
              postgresql_ops={'news_search': 'gin_trgm_ops'},
        ),
    ) 
    
    #               postgresql_ops={'content': 'gin_trgm_ops'}

class NewsAction(Base):
    __tablename__ = "news_actions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"))
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id", ondelete="CASCADE", onupdate="CASCADE"))
    # "create", "edit", "delete"
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
    

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    status: Mapped[str]
    role: Mapped[str]
    position: Mapped[str] = mapped_column(nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    
    user: Mapped["User"] = relationship(lazy="selectin")
    
    
class BaseSettings(BaseClear):
    __tablename__ = "base_settings"
    
    name: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(String(256))