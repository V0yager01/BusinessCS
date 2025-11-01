from src.database.config import async_session

from src.security.exceptions import authorize_exception, json_exception

from .repo import TeamRepo, TeamUserRepo


async def create_team(team_data):
    teamrepo = TeamRepo()
    try:
        await teamrepo.insert_model(team_data)
    except Exception as e:
        raise e


async def get_full_team(uuid):
    teamrepo = TeamRepo()
    try:
        return await teamrepo.get_team_by_uuid(uuid)
    except Exception as e:
        raise e


async def add_user_to_team(usertoteam):
    userteamrepo = TeamUserRepo()
    try:
        await userteamrepo.insert_model(usertoteam)
    except Exception as e:
        raise json_exception


async def remove_user_to_team(uuid):
    userteamrepo = TeamUserRepo()
    try:
        await userteamrepo.delete_model(uuid)
    except Exception as e:
        raise json_exception


async def change_userteam_role(role_change):
    userteamrepo = TeamUserRepo()
    uuid = role_change.get('uuid')
    values = {
        'team_role': role_change.get('team_role')
    }
    try:
        await userteamrepo.update_model(uuid, values)
    except Exception as e:
        raise json_exception
