from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.config import async_session
from src.database.repo import BaseRepo

from .models import TeamUser, Team


class TeamRepo(BaseRepo):
    model = Team

    async def get_team_by_uuid(self, uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(uuid=uuid).options(selectinload(self.model.teamuser).selectinload(TeamUser.user_relation))
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()


class TeamUserRepo(BaseRepo):
    model = TeamUser
