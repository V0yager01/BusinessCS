import asyncio

import pytest
import pytest_asyncio

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database.config import Base, async_engine

from src.team.models import Team, TeamUser
from src.user.models import User
from src.user.repo import UserRepo
from src.task.models import Task, Comment
from src.meeting.models import UserMeeting, Meeting


from src.loader import settings


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