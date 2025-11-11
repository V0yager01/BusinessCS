from uuid import UUID
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database.config import async_session, get_db
from src.user.repo import UserRepo

from .utils import validate_token
from .exceptions import authorize_exception, credentials_exception


security = HTTPBearer()


async def user_auth(credentials: HTTPAuthorizationCredentials = Depends(security),
                    session=Depends(get_db)):
    token = credentials.credentials
    try:
        user_repo = UserRepo(session)
        return await validate_token(token, user_repo)
    except ValueError:
        raise credentials_exception


async def user_is_admin(user: Annotated[str, Depends(user_auth)]):
    if not user.role.value == 'admin':
        raise authorize_exception
    return user


async def user_is_manager(user: Annotated[str, Depends(user_auth)]):
    if not user.role.value == 'manager' or user.role.value == 'admin':
        raise authorize_exception
    return user