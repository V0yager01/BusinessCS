from uuid import uuid4

from src.security.exceptions import register_exception
from src.database.config import async_session
from src.security.utils import create_token, hash_password, check_user_credentials

from .repo import UserRepo


async def create_user(user_data):
    user_repo = UserRepo()
    user_data['password'] = hash_password(user_data['password'])
    try:
        user = await user_repo.create_user(user_data)
        return user
    except ValueError:
        raise register_exception
    except RuntimeError:
        raise RuntimeError


async def get_tokens(user_credentials):
    user_repo = UserRepo()
    user = await user_repo.get_user_by_conditions({"email": user_credentials['email']})
    check_user_credentials(user, user_credentials['password'])
    access_token = create_token(payload_data={"uuid": str(user.uuid),
                                              'type':'access_token'},
                                              expire_delta=1500)
    return {'access_token': access_token}