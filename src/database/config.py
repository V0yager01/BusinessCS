from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.loader import settings

from contextlib import asynccontextmanager

sync_engine = create_engine(settings.pg_url_sync, echo=True)
async_engine = create_async_engine(settings.pg_url, echo=True)
#async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


def async_session():
    return async_sessionmaker(async_engine)