from uuid import uuid4


def test_auth_user(init_user, test_client):
    access_token = init_user
    response = test_client.get(
        "/user/check_auth",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    # endpoint returns current user uuid
    user_uuid = response.json()
    assert isinstance(user_uuid, str)


def test_get_me(init_user, test_client):
    response = test_client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {init_user}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "user1234@g.ru"
    assert body["username"] == "test_user"
    assert body["role"] == "admin"


def test_register_and_login_new_user(test_client):
    unique_id = uuid4().hex
    user_payload = {
        "username": f"user_{unique_id}",
        "email": f"user_{unique_id}@example.com",
        "password": "strong-password",
        "role": "user",
    }
    register_response = test_client.post("/user/register", json=user_payload)
    assert register_response.status_code == 200

    login_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"],
    }
    login_response = test_client.post("/user/get_token", json=login_payload)
    assert login_response.status_code == 200
    token_body = login_response.json()
    assert "access_token" in token_body
