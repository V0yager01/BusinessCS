
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.config import async_session
from src.database.repo import BaseRepo
from src.user.models import User


class UserRepo(BaseRepo):
    model = User
    async_session = async_session()

    async def get_user_by_conditions(self, conditions):
        async with self.async_session() as session:
            query = select(User).filter_by(**conditions)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create_user(self, user_data):
        async with self.async_session() as session:
            try:
                user_model = User(**user_data)
                session.add(user_model)
                await session.commit()
                await session.refresh(user_model)
                return user_data
            except IntegrityError as e:
                raise ValueError(f'Invalid user credentials')
            except SQLAlchemyError as e:
                raise RuntimeError(f'database error: {e}')