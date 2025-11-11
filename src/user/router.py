from typing import Annotated

from fastapi import APIRouter, Depends

from src.database.config import get_db
from src.security.depends import user_auth

from .service import create_user, get_tokens, remove_user
from .schemas import RegisterUserShema, ProvideUserCredShema, TokenResponseShema, ProvideUserCredShema, UserResponseShema


router = APIRouter(
    prefix='/user',
    tags=["auth"]
)


@router.post('/register')
async def register_user(user_data: RegisterUserShema,
                        session=Depends(get_db)) -> UserResponseShema:
    await create_user(user_data.model_dump(), session)
    return user_data


@router.post('/get_token')
async def get_token(user_credentials: ProvideUserCredShema,
                    session=Depends(get_db)) -> TokenResponseShema:
    token = await get_tokens(user_credentials.model_dump(), session)
    return token


@router.delete('/remove')
async def delete_user(user: Annotated[str, Depends(user_auth)],
                      session=Depends(get_db)):
    await remove_user(user.uuid, session)


@router.get('/check_auth')
async def check_token(user_uuid: Annotated[str, Depends(user_auth)]):
    return user_uuid