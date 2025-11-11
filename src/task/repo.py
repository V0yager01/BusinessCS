from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.config import async_session
from src.database.repo import BaseRepo

from .models import Task, Comment


class TaskRepo(BaseRepo):
    model = Task

    async def select_full_task_by_uuid(self, uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(uuid=uuid).options(selectinload(self.model.comments))
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

class CommentRepo(BaseRepo):
    async_session = async_session
    model = Comment
