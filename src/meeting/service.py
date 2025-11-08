from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from src.security.exceptions import json_exception

from .repo import UserMeetingRepo, MeetingRepo


async def create_meeting(time):
    repo = MeetingRepo()
    minutes = time.get('meet_duration_minutes', 0)
    hours = time.get('meet_duration_hour', 0)
    start_at = time['start_at']
    end_at = start_at + timedelta(hours=hours,
                                  minutes=minutes)
    try:
        meet = await repo.insert_model({
            'start_at': start_at,
            'end_at': end_at
        })
        return meet
    except Exception as e:
        raise e


async def append_users_to_meeting(meeting_uuid, users):
    usermeetrepo = UserMeetingRepo()
    success = []
    error = []
    meet_model = await get_meet(meeting_uuid)
    meet_time = {'start_at': meet_model.start_at,
                 'end_at': meet_model.end_at}
    for user_uuid in users['uuid']:
        reserved_times = []
        meets_model = await get_user_meet_list(user_uuid)
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


async def remove_meeting(meeting_uuid):
    meetrepo = MeetingRepo()
    try:
        await meetrepo.delete_model(meeting_uuid)
    except Exception as e:
        raise e


def is_user_free(user_reserved_time, meeting_time):
    for time in user_reserved_time:
        if time['start_at'] < meeting_time['start_at'] or time['end_at'] > meeting_time['end_at']:
            return False
    return True


async def get_user_meet_list(user_uuid):
    usermeetrepo = UserMeetingRepo()
    try:
        user_meets = await usermeetrepo.select_time_by_useruuid(user_uuid)
        return user_meets
    except Exception as e:
        raise e


async def get_meet(meet_uuid):
    meetrepo = MeetingRepo()
    try:
        meet = await meetrepo.select_model_by_uuid(meet_uuid)
        return meet
    except Exception as e:
        raise e
