from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.security.depends import user_auth

from .service import create_meeting, append_users_to_meeting, get_user_meet_list, remove_meeting
from .schemas import CreateMeetingBaseShema, UsersToInviteShema

router = APIRouter(
    prefix='/meeting',
    tags=['meetings']
)


@router.post('')
async def post_meeting(meet_schema: CreateMeetingBaseShema):
    response = await create_meeting(meet_schema.model_dump())
    return response


@router.post('/{meeting_uuid}/invite')
async def invite_user(meeting_uuid: UUID,
                      userstoinvite_shema: UsersToInviteShema):
    res = await append_users_to_meeting(meeting_uuid=meeting_uuid, users=userstoinvite_shema.model_dump())
    return res


@router.get('/mymeetings')
async def get_user_meetings(user: Annotated[str, Depends(user_auth)]):
    meetings = await get_user_meet_list(user.uuid)
    return meetings


@router.delete('')
async def delete_meeting(meeting_uuid: UUID,
                         user: Annotated[str, Depends(user_auth)]):
    await remove_meeting(meeting_uuid)