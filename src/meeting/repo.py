from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.database.repo import BaseRepo

from .models import Meeting, UserMeeting


class MeetingRepo(BaseRepo):
    model = Meeting


class UserMeetingRepo(BaseRepo):
    model = UserMeeting

    async def get_all_user_meet_time(self, user_uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(user_uuid=user_uuid).options(selectinload(self.model.meeting))
            result = session.execute(query)
            return result.unique().scalars().all()

    async def insert_many_users(self, meeting_uuid, users):
        async with self.async_session as session:
            objects = [
                self.model(meeting_uuid=meeting_uuid, user_uuid=user_uuid) for user_uuid in users['uuid']
            ]
            session.add_all(objects)
            await session.commit()

    async def select_time_by_useruuid(self, user_uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(user_uuid=user_uuid).options(joinedload(self.model.meeting))
            result = await session.execute(query)
            return result.scalars().all()