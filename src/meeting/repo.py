from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload, joinedload

from src.database.repo import BaseRepo

from .models import Meeting, UserMeeting


class MeetingRepo(BaseRepo):
    model = Meeting


class UserMeetingRepo(BaseRepo):
    model = UserMeeting

    async def get_all_user_meet_time(self, user_uuid):
        async with self.async_session as session:
            query = (
                select(self.model)
                .filter_by(user_uuid=user_uuid)
                .options(
                    selectinload(self.model.meeting).selectinload(Meeting.participants)
                )
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def insert_many_users(self, meeting_uuid, users):
        async with self.async_session as session:
            try:
                objects = [
                    self.model(meeting_uuid=meeting_uuid, user_uuid=user_uuid) for user_uuid in users['uuid']
                ]
                session.add_all(objects)
                await session.commit()
            except IntegrityError as e:
                raise e
            except SQLAlchemyError as e:
                raise RuntimeError(f'database error: {e}')

    async def select_time_by_useruuid(self, user_uuid):
        async with self.async_session as session:
            query = (
                select(self.model)
                .filter_by(user_uuid=user_uuid)
                .options(
                    joinedload(self.model.meeting).selectinload(Meeting.participants)
                )
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def get_participant(self, meeting_uuid, user_uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(
                meeting_uuid=meeting_uuid,
                user_uuid=user_uuid
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def delete_participant(self, meeting_uuid, user_uuid):
        async with self.async_session as session:
            query = delete(self.model).filter_by(
                meeting_uuid=meeting_uuid,
                user_uuid=user_uuid
            )
            await session.execute(query)
            await session.commit()