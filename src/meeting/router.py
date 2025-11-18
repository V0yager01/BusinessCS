from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.database.config import get_db
from src.security.depends import user_auth

from .service import (
    create_meeting,
    append_users_to_meeting,
    get_user_meet_list,
    remove_meeting,
    update_meeting,
    remove_participant_from_meeting
)
from .schemas import (
    CreateMeetingBaseShema,
    MeetingResponseShema,
    UsersToInviteShema,
    UpdateMeetingShema,
    MeetingParticipantShema,
    UserMeetingResponseShema,
)

router = APIRouter(
    prefix='/meeting',
    tags=['meetings']
)


@router.post('')
async def post_meeting(meet_schema: CreateMeetingBaseShema,
                       user: Annotated[str, Depends(user_auth)],
                       session=Depends(get_db)) -> MeetingResponseShema:
    response = await create_meeting(
        meet_schema.model_dump(),
        user.uuid,
        session
    )
    return MeetingResponseShema.model_validate(response)


@router.post('/{meeting_uuid}/invite')
async def invite_user(meeting_uuid: UUID,
                      userstoinvite_shema: UsersToInviteShema,
                      user: Annotated[str, Depends(user_auth)],
                      session=Depends(get_db)):
    res = await append_users_to_meeting(meeting_uuid,
                                        userstoinvite_shema.model_dump(),
                                        session)
    return res


@router.get('/mymeetings')
async def get_user_meetings(user: Annotated[str, Depends(user_auth)],
                            session=Depends(get_db)) -> list[UserMeetingResponseShema]:
    meetings = await get_user_meet_list(user.uuid, session)
    return [
        UserMeetingResponseShema.model_validate(record)
        for record in meetings
    ]


@router.delete('', status_code=204)
async def delete_meeting(meeting_uuid: UUID,
                         user: Annotated[str, Depends(user_auth)],
                         session=Depends(get_db)):
    await remove_meeting(meeting_uuid, session)
    return {'detail': 'meeting deleted'}


@router.patch('/{meeting_uuid}')
async def patch_meeting(meeting_uuid: UUID,
                        meet_schema: UpdateMeetingShema,
                        user: Annotated[str, Depends(user_auth)],
                        session=Depends(get_db)) -> MeetingResponseShema:
    response = await update_meeting(
        meeting_uuid,
        meet_schema.model_dump(),
        user.uuid,
        session
    )
    return MeetingResponseShema.model_validate(response)


@router.delete('/{meeting_uuid}/participant')
async def delete_meeting_participant(meeting_uuid: UUID,
                                     participant: MeetingParticipantShema,
                                     user: Annotated[str, Depends(user_auth)],
                                     session=Depends(get_db)):
    await remove_participant_from_meeting(
        meeting_uuid,
        participant.user_uuid,
        user.uuid,
        session
    )
    return {'detail': 'participant removed'}
