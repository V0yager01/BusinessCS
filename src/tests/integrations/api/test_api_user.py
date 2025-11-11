import pytest


def test_auth_user(init_user, test_client):
    access_token = init_user
    response = test_client.get('/user/check_auth',headers={"Authorization": f"Bearer {access_token}"})
    response.status_code == 200
