import pytest

from src.team.repo import TeamRepo

@pytest.fixture()
def test_create_team():
    return {
        "name": "test-team",
        "description": "My test team"
        }


@pytest.fixture(scope='function')
async def get_first_team_uuid():
    teamrepo = TeamRepo()
    team = await teamrepo.select_first_record()
    return team.uuid
