from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.loader import settings

async_engine = create_async_engine(settings.pg_url, echo=True)
async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


async def get_session_factory():
    yield async_session