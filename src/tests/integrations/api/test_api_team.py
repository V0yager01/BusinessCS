import pytest


@pytest.mark.parametrize(
    "user_fixture, expected_status, expected_name",
    [
        ("manager_user", 200, "Team created by manager_user"),
        ("init_user", 403, None),
        ("regular_user", 403, None),
    ],
)
def test_register_team_permissions(test_client, request, user_fixture, expected_status, expected_name):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"name": f"Team created by {user_fixture}"}
    response = test_client.post("/team", json=payload, headers=headers)
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        assert body["name"] == expected_name
        assert "uuid" in body


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("init_user", 403),
        ("regular_user", 403),
    ],
)
def test_invite_user_permissions(test_client, request, user_fixture, expected_status):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"team_uuid": "some-team-uuid", "user_uuid": "some-user-uuid", "role": "member"}
    response = test_client.post("/team/user", json=payload, headers=headers)
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        assert body["team_uuid"] == payload["team_uuid"]
        assert body["user_uuid"] == payload["user_uuid"]
        assert body["role"] == payload["role"]


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("init_user", 403),
        ("regular_user", 403),
    ],
)
def test_remove_user_permissions(test_client, request, user_fixture, expected_status):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    params = {"userteamuuid": "some-userteam-uuid"}
    response = test_client.delete("/team/user", params=params, headers=headers)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_fixture, expected_status, expected_role",
    [
        ("manager_user", 200, "manager"),
        ("init_user", 403, None),
        ("regular_user", 403, None),
    ],
)
def test_update_role_permissions(test_client, request, user_fixture, expected_status, expected_role):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"userteamuuid": "some-userteam-uuid", "role": "manager"}
    response = test_client.patch("/team/user", json=payload, headers=headers)
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        assert body["userteamuuid"] == payload["userteamuuid"]
        assert body["role"] == expected_role


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("init_user", 200),
        ("regular_user", 200),
    ],
)
def test_get_team_permissions(test_client, request, user_fixture, expected_status):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    params = {"team_uuid": "some-team-uuid"}
    response = test_client.get("/team", params=params, headers=headers)
    assert response.status_code == expected_status
    if expected_status == 200 and response.status_code == 200:
        body = response.json()
        assert body["uuid"] == params["team_uuid"]
