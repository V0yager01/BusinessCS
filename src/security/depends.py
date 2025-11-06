from uuid import UUID
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database.config import async_session
from src.user.repo import UserRepo

from .utils import validate_token
from .exceptions import authorize_exception, credentials_exception


security = HTTPBearer()


async def user_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_repo = UserRepo()
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



# async def get_current_user(token: Annotated[str, Header(alias='Authorization')]):
#     payload = decode_token(token)
#     if payload.get('type') != 'access_token':
#         raise credentials_exception
#     id = payload.get('id')
#     user = await UserDao.get_user({"id":id})
#     if not user:
#         raise credentials_exception
#     return id


# async def rotate_tokens(request: Request):
#     token = request.headers.get('authorization')
#     payload = decode_token(token)
#     if payload.get('type') != 'refresh_token' or await check_token_black_list(token):
#         raise credentials_exception
#     id = payload.get('id')
#     await black_list_add(token=token, token_type="refresh_token", expire_time=60)
#     new_access_token = create_token(payload_data={"id":id, 'type':'access_token'}, expire_delta=15)
#     new_refresh_token = create_token(payload_data={"id":id, 'type':'refresh_token'}, expire_delta=60)

#     return {
#         "access_token": new_access_token,
#         "refresh_token": new_refresh_token
#     }