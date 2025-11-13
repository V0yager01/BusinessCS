from src.security.exceptions import json_exception

from .repo import TeamRepo, TeamUserRepo
from .models import TeamRole


async def create_team(team_data, user_uuid, session):
    teamrepo = TeamRepo(session)
    userteamrepo = TeamUserRepo(session)
    try:
        team = await teamrepo.insert_model(team_data)
        await userteamrepo.insert_model({
            'team': team.uuid,
            'user': user_uuid,
            'team_role': TeamRole.manager
        })
        return team
    except Exception as e:
        raise json_exception


async def get_full_team(uuid, session):
    teamrepo = TeamRepo(session)
    try:
        return await teamrepo.get_team_by_uuid(uuid)
    except Exception:
        raise json_exception


async def add_user_to_team(usertoteam, session):
    userteamrepo = TeamUserRepo(session)
    try:
        await userteamrepo.insert_model(usertoteam)
    except Exception:
        raise json_exception


async def remove_user_to_team(uuid, session):
    userteamrepo = TeamUserRepo(session)
    try:
        await userteamrepo.delete_model(uuid)
    except Exception:
        raise json_exception


async def change_userteam_role(role_change, session):
    userteamrepo = TeamUserRepo(session)
    uuid = role_change.get('uuid')
    values = {
        'team_role': role_change.get('team_role')
    }
    try:
        await userteamrepo.update_model(uuid, values)
    except Exception as e:
        raise json_exception


async def get_user_teams(user_uuid, session):
    userteamrepo = TeamUserRepo(session)
    try:
        team_users = await userteamrepo.get_team_users_by_user_uuid(user_uuid)
        teams_data = []
        for team_user in team_users:
            team = await get_full_team(team_user.team, session)
            if team:
                teams_data.append({
                    'team': team,
                    'team_role': team_user.team_role,
                    'team_user_uuid': team_user.uuid
                })
        return teams_data
    except Exception as e:
        raise json_exception
