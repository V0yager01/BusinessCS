from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.repo import BaseRepo

from .models import Task, Comment


class TaskRepo(BaseRepo):
    model = Task

    async def select_full_task_by_uuid(self, uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(uuid=uuid).options(selectinload(self.model.comments))
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    async def get_tasks_by_team_uuid(self, team_uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(team=team_uuid).options(selectinload(self.model.comments))
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def get_tasks_by_user_uuid(self, user_uuid):
        async with self.async_session as session:
            query = select(self.model).filter(
                (self.model.performer == user_uuid) | (self.model.author == user_uuid)
            ).options(selectinload(self.model.comments))
            result = await session.execute(query)
            return result.unique().scalars().all()


class CommentRepo(BaseRepo):
    model = Comment
