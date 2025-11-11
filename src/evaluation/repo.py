from sqlalchemy import update, insert, select, and_, func

from src.database.config import async_session
from src.database.repo import BaseRepo

from src.task.models import Task

from .models import Evaluation


class EvaluationRepo(BaseRepo):
    model = Evaluation

    async def insert_evaluation_and_update_task(self, task_uuid, values):
        async with async_session as session:
            await session.execute(
                update(Task).filter_by(uuid=task_uuid).values(status='done')
            )

            evaluation = self.model(**values)
            session.add(evaluation)
            await session.commit()
            await session.refresh(evaluation)
            return evaluation

    async def select_all_evaluation_by_dates(self,
                                             user_uuid,
                                             start_date,
                                             end_date):
        async with async_session as session:
            query = select(self.model).where(and_(self.model.performer == user_uuid,
                                                  self.model.created_at.between(start_date, end_date)))
            result = await session.execute(query)
            return result.scalars().all()

    async def select_avg_rate(self, user_uuid):
        async with async_session as session:
            query = select(func.avg(self.model.rate).label('avg-rate')).filter_by(performer=user_uuid).group_by(self.model.performer)
            result = await session.execute(query)
            return result.mappings().first()