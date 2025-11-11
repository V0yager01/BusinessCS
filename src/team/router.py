from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.database.config import get_db
from src.security.depends import user_auth, user_is_manager
from src.security.exceptions import exception_404

from .service import create_team, add_user_to_team, remove_user_to_team, change_userteam_role, get_full_team
from .shemas import TeamBaseShema, AddUserToTeamShema, UpdateRoleUserToTeamShema, TeamResponseShema, CreateTeamResponseShema

router = APIRouter(
    prefix='/team',
    tags=['team']
)


@router.get('')
async def get_team(team_uuid: UUID,
                   user: Annotated[str, Depends(user_auth)],
                   session=Depends(get_db)) -> TeamResponseShema:
    team = await get_full_team(team_uuid, session)
    if not team:
        raise exception_404
    response_team_shema = TeamResponseShema.model_validate(team)
    return response_team_shema


@router.post('')
async def register_team(team: TeamBaseShema,
                        user: Annotated[str, Depends(user_is_manager)],
                        session=Depends(get_db)) -> CreateTeamResponseShema:
    team = await create_team(team.model_dump(), session)
    return team


@router.post('/user')
async def invite_user(usertoteam: AddUserToTeamShema,
                      user: Annotated[str, Depends(user_is_manager)],
                      session=Depends(get_db)) -> AddUserToTeamShema:
    await add_user_to_team(usertoteam.model_dump(), session)
    return usertoteam


@router.delete('/user')
async def remove_user(userteamuuid: UUID,
                      user: Annotated[str, Depends(user_is_manager)],
                      session=Depends(get_db)) -> None:
    await remove_user_to_team(userteamuuid, session)
    return None


@router.patch('/user')
async def update_role(role_update: UpdateRoleUserToTeamShema,
                      user: Annotated[str, Depends(user_is_manager)],
                      session=Depends(get_db)) -> UpdateRoleUserToTeamShema:
    await change_userteam_role(role_update.model_dump(), session)
    return role_update
