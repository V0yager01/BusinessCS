from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBaseShema(BaseModel):
    username: str


class RegisterUserShema(UserBaseShema):
    email: EmailStr
    password: str


class UserResponseShema(UserBaseShema):
    pass


class TokenResponseShema(BaseModel):
    access_token: str
    refresh_token: str


class ProvideUserCredShema(BaseModel):
    email: EmailStr
    password: str
