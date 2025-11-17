from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class BaseRepo():
    model = None

    def __init__(self, session):
        self.async_session = session

    async def select_model_by_uuid(self, uuid):
        async with self.async_session as session:
            query = select(self.model).filter_by(uuid=uuid)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def insert_model(self, data):
        async with self.async_session as session:
            try:
                task = self.model(**data)
                session.add(task)
                await session.commit()
                await session.refresh(task)
                return task
            except IntegrityError as e:
                raise e
            except SQLAlchemyError as e:
                raise RuntimeError(f'database error: {e}')

    async def update_model(self, uuid, values):
        async with self.async_session as session:
            try:
                query = update(self.model).filter_by(uuid=uuid).values(**values)
                await session.execute(query)
                await session.commit()
            except IntegrityError as e:
                raise ValueError('Invalid data values')
            except SQLAlchemyError as e:
                raise RuntimeError(f'database error: {e}')

    async def delete_model(self, uuid):
        async with self.async_session as session:
            try:
                query = delete(self.model).filter_by(uuid=uuid)
                await session.execute(query)
                await session.commit()
            except IntegrityError:
                raise ValueError('Invalid parametrs')
            except Exception as e:
                raise e
