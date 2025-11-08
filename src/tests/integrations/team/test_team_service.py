from src.team.service import (
    create_team,
    get_full_team,
    add_user_to_team,
    remove_user_to_team,
    change_userteam_role,
)


async def test_create_team(test_team_data):
    team = await create_team(test_team_data)
    assert team


# async def test_get_team_by_uuid(test_team_uuid):
#     team = await get_full_team(test_team_uuid)
#     assert team


# async def test_add_and_remove_member(test_team_uuid, test_user_uuid, session_db):
#     added = await add_user_to_team(test_team_uuid, test_user_uuid)
#     assert added

#     removed = await remove_user_to_team(test_team_uuid, test_user_uuid)
#     assert removed


# async def test_change_userteam_role(test_team_uuid, session_db):
#     values = {"name": "updated-name"}
#     updated = await change_userteam_role(test_team_uuid, values)
#     assert updated
#     assert getattr(updated, "name", None) == "updated-name"