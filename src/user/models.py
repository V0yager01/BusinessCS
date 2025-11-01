from enum import Enum as PyEnum
from uuid import UUID

from sqlalchemy import String, UUID, Integer, Enum, text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.config import Base


class Role(PyEnum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(256), unique=False, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user)
    password: Mapped[str] = mapped_column(String, unique=False)
