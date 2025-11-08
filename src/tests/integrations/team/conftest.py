import pytest



@pytest.fixture()
def test_team_data():
    return {
        "name":"test-team",
        "description": "My test team"
        }

