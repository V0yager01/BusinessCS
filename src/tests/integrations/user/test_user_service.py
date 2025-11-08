
import pytest

from src.user.service import create_user, get_tokens


@pytest.mark.skip
async def test_create_user(test_user_data, test_session):
    user_model = await create_user(test_user_data)
    assert user_model


async def test_get_tokens(test_user_cred, test_session):
    token = await get_tokens(test_user_cred)
    assert token

def test():
    assert 1 == 1