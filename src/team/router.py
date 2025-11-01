from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.security.depends import user_auth, user_is_admin

from .service import create_team, add_user_to_team, remove_user_to_team, change_userteam_role, get_full_team
from .shemas import TeamBaseShema, AddUserToTeamShema, UpdateRoleUserToTeamShema, TeamResponseShema

router = APIRouter(
    prefix='/team',
    tags=['team']
)


@router.get('')
async def get_team(team_uuid: UUID, user: Annotated[str, Depends(user_is_admin)]) -> TeamResponseShema:
    team = await get_full_team(team_uuid)
    response_team_shema = TeamResponseShema.model_validate(team)
    return response_team_shema


@router.post('')
async def register_team(team: TeamBaseShema, user: Annotated[str, Depends(user_is_admin)]):
    await create_team(team_data=team.model_dump())
    return team


@router.post('/user')
async def invite_user(usertoteam: AddUserToTeamShema, user: Annotated[str, Depends(user_is_admin)]):
    await add_user_to_team(usertoteam=usertoteam.model_dump())
    return usertoteam


@router.delete('/user')
async def remove_user(userteamuuid: UUID, user: Annotated[str, Depends(user_is_admin)]):
    await remove_user_to_team(userteamuuid)
    return None


@router.patch('/user')
async def update_role(role_update: UpdateRoleUserToTeamShema, user: Annotated[str, Depends(user_is_admin)]):
    await change_userteam_role(role_update.model_dump())
    return role_update


