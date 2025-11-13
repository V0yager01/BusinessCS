from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext


from src.loader import settings
from .exceptions import credentials_exception, auth_exception


pwd = CryptContext(schemes=['bcrypt'])
secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM


def hash_password(password: str):
    return pwd.hash(password)


def verify_password(current_password: str, db_password: str):
    return pwd.verify(current_password, db_password)


def create_token(payload_data: dict, expire_delta: int = 15):
    data_encode = payload_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    data_encode.update({'exp': expire})
    encode = jwt.encode(data_encode, secret_key, algorithm=algorithm)
    return encode


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm)
    except InvalidTokenError:
        raise credentials_exception
    return payload


def check_user_credentials(user,  password):
    if not user:
        raise auth_exception
    elif not verify_password(password, user.password):
        raise auth_exception


async def validate_token(token: str, user_repo):
    payload = decode_token(token)
    if payload.get('type') != 'access_token':
        raise ValueError('invalid token')
    uuid = payload.get('uuid')
    user = await user_repo.get_user_by_conditions({"uuid": uuid})
    if not user:
        raise ValueError('invalid token')
    return user


def check_is_author(task_author, user_uuid):
    return task_author == user_uuid