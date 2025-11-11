from fastapi.testclient import TestClient
import pytest

from src.main import app


@pytest.fixture(scope='session')
def test_client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='session', autouse=True)
def init_user(test_client):
    user_cred = {"username": "test_user",
                 "email": "user1234@g.ru",
                 "password": "string",
                 "role": "admin"}
    response = test_client.post("/user/register", json=user_cred)
    assert response.status_code == 200
    access_token = test_client.post("/user/get_token",
                                    json={
                                        "email": user_cred['email'],
                                        "password": user_cred['password']
                                    })
    access_token = access_token.json()['access_token']
    yield access_token
    test_client.delete('/user/remove',
                       headers={"Authorization": f"Bearer {access_token}"}
                       )


@pytest.fixture(scope='session', autouse=True)
def regular_user(test_client):
    user_cred = {"username": "test_user1",
                 "email": "user12345@g.ru",
                 "password": "string",
                 "role": "user"}
    response = test_client.post("/user/register", json=user_cred)
    assert response.status_code == 200
    access_token = test_client.post("/user/get_token",
                                    json={
                                        "email": user_cred['email'],
                                        "password": user_cred['password']
                                    })
    access_token = access_token.json()['access_token']
    yield access_token
    test_client.delete('/user/remove',
                       headers={"Authorization": f"Bearer {access_token}"}
                       )



@pytest.fixture(scope='session', autouse=True)
def manager_user(test_client):
    user_cred = {"username": "test_user2",
                 "email": "user1234566@g.ru",
                 "password": "string",
                 "role": "manager"}
    response = test_client.post("/user/register", json=user_cred)
    assert response.status_code == 200
    access_token = test_client.post("/user/get_token",
                                    json={
                                        "email": user_cred['email'],
                                        "password": user_cred['password']
                                    })
    access_token = access_token.json()['access_token']
    yield access_token
    test_client.delete('/user/remove',
                       headers={"Authorization": f"Bearer {access_token}"}
                       )