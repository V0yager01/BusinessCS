from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskStatus(str, Enum):
    waiting = 'waiting'
    in_progress = 'in progress'
    done = 'done'


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    status: TaskStatus
    deadline: datetime
    team: UUID


class CreateTaskShemas(TaskBase):
    pass


class UpdateTaskShema(TaskBase):
    title: str | None
    description: str | None
    status: TaskStatus | None
    deadline: datetime | None
    performer: UUID | None = None


class SetPerformerShema(BaseModel):
    performer: UUID


class SetStatusShema(BaseModel):
    status: TaskStatus


class CommentBaseShema(BaseModel):
    text: str


class CommentResponseShema(CommentBaseShema):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    author: UUID


class TaskResponse(TaskBase):
    uuid: UUID | None
    performer: UUID | None
    author: UUID | None


class TaskCommentsResponse(TaskResponse):
    comments: list[CommentResponseShema] | None
