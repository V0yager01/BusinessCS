
import pytest

from src.user.service import create_user, get_tokens


@pytest.mark.skip
async def test_create_user(test_user_data):
    user_model = await create_user(test_user_data)
    assert user_model


async def test_get_tokens(test_user_cred):
    token = await get_tokens(test_user_cred)
    assert token