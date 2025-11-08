import pytest
import pytest_asyncio

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database import config


from src.loader import settings


class Base(DeclarativeBase):
    pass


@pytest.fixture(scope='function')
async def test_session(monkeypatch):
    async_engine = create_async_engine(settings.pg_url, echo=True)
    async_session = async_sessionmaker(async_engine)
    print("До:", config.async_session)
    monkeypatch.setattr(config, 'async_session', async_session)
    print("После:", config.async_session)
    yield async_session



@pytest.fixture()
def test_user_data():
    return {
        "username": "string",
        "email": "user@example.com",
        "password": "string"
        }

@pytest.fixture()
def test_user_cred():
    return {
        "email": "user@example.com",
        "password": "string"
        }