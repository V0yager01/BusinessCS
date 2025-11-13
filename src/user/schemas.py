from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBaseShema(BaseModel):
    username: str


class RegisterUserShema(UserBaseShema):
    email: EmailStr
    password: str
    role: str = Field(default='user')

class UserResponseShema(UserBaseShema):
    pass


class TokenResponseShema(BaseModel):
    access_token: str


class ProvideUserCredShema(BaseModel):
    email: EmailStr
    password: str


class UserProfileShema(BaseModel):
    uuid: UUID
    username: str
    email: EmailStr
    role: str
    
    model_config = ConfigDict(from_attributes=True)
    
    # @classmethod
    # def from_orm(cls, obj):
    #     data = {
    #         'uuid': obj.uuid,
    #         'username': obj.username,
    #         'email': obj.email,
    #         'role': obj.role.value if hasattr(obj.role, 'value') else str(obj.role)
    #     }
    #     return cls(**data)