from enum import Enum as PyEnum

from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class TeamRole(str, PyEnum):
    employee = 'employee'
    manager = 'manager'


class UserRole(str, PyEnum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class TeamBaseShema(BaseModel):
    name: str
    description: str | None = None


class TeamResponseShema(BaseModel):
    uuid: UUID
    name: str
    description: str
    teamuser: list['UserTeamResponseShema']

    model_config = ConfigDict(from_attributes=True)


class UserTeamResponseShema(BaseModel):
    uuid: UUID
    team_role: TeamRole
    user_relation: 'UserResponseShema'

    model_config = ConfigDict(from_attributes=True)


class UserResponseShema(BaseModel):
    uuid: UUID
    username: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserToTeamBase(BaseModel):
    team: UUID = Field(alias='team_uuid')
    user: UUID = Field(alias='user_uuid')


class AddUserToTeamShema(UserToTeamBase):
    team_role: TeamRole


class UpdateRoleUserToTeamShema(BaseModel):
    uuid: UUID
    team_role: TeamRole

class GetUserTeamListShema(BaseModel):
    pass


class PromoteUserTeamShema(BaseModel):
    pass


class GetTeamListShema(BaseModel):
    pass