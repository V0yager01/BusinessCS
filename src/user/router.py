from typing import Annotated

from fastapi import APIRouter, Depends

from src.security.depends import user_auth

from .service import create_user, get_tokens
from .schemas import RegisterUserShema, ProvideUserCredShema, TokenResponseShema, ProvideUserCredShema, UserResponseShema

router = APIRouter(
    prefix='/user',
    tags=["auth"]
)


@router.post('/register')
async def register_user(user_data: RegisterUserShema) -> UserResponseShema:
    await create_user(user_data.model_dump())
    return user_data


@router.post('/get_token')
async def get_token(user_credentials: ProvideUserCredShema) -> TokenResponseShema:
    token = await get_tokens(user_credentials.model_dump())
    return token


@router.get('/check_auth')
async def check_token(user_uuid: Annotated[str, Depends(user_auth)]):
    return user_uuid