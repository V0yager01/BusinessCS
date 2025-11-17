from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError

from src.security.exceptions import authorize_exception, exception_404

from .repo import UserMeetingRepo, MeetingRepo


async def create_meeting(time, user_uuid, session):
    repo = MeetingRepo(session)
    usermeetrepo = UserMeetingRepo(session)
    minutes = time.get('meet_duration_minutes', 0)
    hours = time.get('meet_duration_hour', 0)
    start_at = time['start_at']

    if not isinstance(start_at, datetime):
        raise ValueError("start_at должен быть datetime объектом")

    if start_at.tzinfo is None:
        start_at = start_at.replace(tzinfo=timezone.utc)

    end_at = start_at + timedelta(hours=hours, minutes=minutes)

    try:
        meet = await repo.insert_model({
            'start_at': start_at,
            'end_at': end_at
        })

        await usermeetrepo.insert_model({
            'meeting_uuid': meet.uuid,
            'user_uuid': user_uuid
        })

        return meet
    except Exception as e:
        raise e


async def append_users_to_meeting(meeting_uuid, users, session):
    usermeetrepo = UserMeetingRepo(session)
    success = []
    error = []
    meet_model = await get_meet(meeting_uuid, session)
    meet_time = {'start_at': meet_model.start_at,
                 'end_at': meet_model.end_at}
    for user_uuid in users['uuid']:
        reserved_times = []
        meets_model = await get_user_meet_list(user_uuid, session)
        for meet in meets_model:
            reserved_times.append({'start_at': meet.meeting.start_at,
                                   'end_at': meet.meeting.end_at})
        if is_user_free(reserved_times, meet_time):
            try:
                await usermeetrepo.insert_model({
                    'meeting_uuid': meeting_uuid,
                    'user_uuid': user_uuid
                })
                success.append(user_uuid)
            except IntegrityError:
                error.append(user_uuid)
            except Exception as e:
                raise e
        else:
            error.append(user_uuid)
    return {'success': success,
            'error': error}


async def remove_meeting(meeting_uuid, session):
    meetrepo = MeetingRepo(session)
    try:
        await meetrepo.delete_model(meeting_uuid)
    except Exception as e:
        raise e


async def update_meeting(meeting_uuid, payload, user_uuid, session):
    repo = MeetingRepo(session)
    usermeetrepo = UserMeetingRepo(session)
    participant = await usermeetrepo.get_participant(meeting_uuid, user_uuid)
    if not participant:
        raise authorize_exception

    start_at = payload['start_at']
    if not isinstance(start_at, datetime):
        raise ValueError("start_at должен быть datetime объектом")

    if start_at.tzinfo is None:
        start_at = start_at.replace(tzinfo=timezone.utc)

    minutes = payload.get('meet_duration_minutes', 0)
    hours = payload.get('meet_duration_hour', 0)
    end_at = start_at + timedelta(hours=hours, minutes=minutes)

    await repo.update_model(meeting_uuid, {
        'start_at': start_at,
        'end_at': end_at
    })

    updated = await repo.select_model_by_uuid(meeting_uuid)
    return updated


async def remove_participant_from_meeting(meeting_uuid, target_uuid, user_uuid, session):
    usermeetrepo = UserMeetingRepo(session)
    participant = await usermeetrepo.get_participant(meeting_uuid, user_uuid)
    if not participant:
        raise authorize_exception

    target = await usermeetrepo.get_participant(meeting_uuid, target_uuid)
    if not target:
        raise exception_404

    await usermeetrepo.delete_participant(meeting_uuid, target_uuid)


def is_user_free(user_reserved_time, meeting_time):
    for reserved_time in user_reserved_time:
        start_overlaps = (
            reserved_time['end_at'] > meeting_time['start_at'] and
            reserved_time['start_at'] < meeting_time['end_at']
        )
        if start_overlaps:
            return False
    return True


async def get_user_meet_list(user_uuid, session):
    usermeetrepo = UserMeetingRepo(session)
    try:
        user_meets = await usermeetrepo.select_time_by_useruuid(user_uuid)
        return user_meets
    except Exception as e:
        raise e


async def get_meet(meet_uuid, session):
    meetrepo = MeetingRepo(session)
    try:
        meet = await meetrepo.select_model_by_uuid(meet_uuid)
        return meet
    except Exception as e:
        raise e
