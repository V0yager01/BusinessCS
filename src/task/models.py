from datetime import datetime
from enum import Enum as PyEnum
from uuid import UUID

from sqlalchemy import String, UUID, Enum, text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.config import Base


class TaskStatus(str, PyEnum):
    waiting = 'waiting'
    in_progress = 'in progress'
    done = 'done'


class Task(Base):
    __tablename__ = 'tasks'

    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    performer: Mapped[UUID | None] = mapped_column(ForeignKey('users.uuid', ondelete='SET NULL'))
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), server_default=TaskStatus.waiting)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    author: Mapped[UUID | None] = mapped_column(ForeignKey('users.uuid', ondelete='CASCADE'))
    comments: Mapped[list['Comment']] = relationship('Comment')


class Comment(Base):
    __tablename__ = 'comments'
    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    author: Mapped[UUID | None] = mapped_column(ForeignKey('users.uuid', ondelete='SET NULL'))
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    task: Mapped[UUID] = mapped_column(ForeignKey('tasks.uuid', ondelete='CASCADE'))
