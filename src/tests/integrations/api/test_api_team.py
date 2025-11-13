import uuid

import pytest


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_team(test_client, manager_token: str) -> dict:
    team_name = f"Team {uuid.uuid4()}"
    payload = {"name": team_name, "description": "Test team"}
    response = test_client.post(
        "/team",
        json=payload,
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == team_name
    return body


def _get_user_uuid(test_client, token: str) -> str:
    response = test_client.get(
        "/user/me",
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    return response.json()["uuid"]


def _get_team_membership(
    test_client,
    team_uuid: str,
    manager_token: str,
    member_uuid: str,
) -> dict | None:
    response = test_client.get(
        "/team",
        params={"team_uuid": team_uuid},
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200
    team_body = response.json()
    for team_user in team_body.get("teamuser", []):
        if team_user["user_relation"]["uuid"] == member_uuid:
            return team_user
    return None


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("regular_user", 403),
    ],
)
def test_register_team_permissions(
    test_client,
    request,
    user_fixture,
    expected_status,
):
    token = request.getfixturevalue(user_fixture)
    team_name = f"Team created by {user_fixture}"
    payload = {"name": team_name, "description": "Permissions test"}
    response = test_client.post(
        "/team",
        json=payload,
        headers=_auth_headers(token),
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        assert body["name"] == team_name
        assert body['uuid']


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("regular_user", 403),
    ],
)
def test_invite_user_permissions(
    test_client,
    request,
    user_fixture,
    expected_status,
    manager_user,
    regular_user,
):
    manager_token = manager_user
    team = _create_team(test_client, manager_token)
    invitee_uuid = _get_user_uuid(test_client, regular_user)

    acting_token = request.getfixturevalue(user_fixture)
    payload = {
        "team_uuid": team["uuid"],
        "user_uuid": invitee_uuid,
        "team_role": "employee",
    }
    response = test_client.post(
        "/team/user",
        json=payload,
        headers=_auth_headers(acting_token),
    )
    assert response.status_code == expected_status

    if expected_status == 200:
        body = response.json()
        # FastAPI serialises aliases by default
        assert body["team_uuid"] == team["uuid"]
        assert body["user_uuid"] == invitee_uuid
        assert body["team_role"] == "employee"
        # cleanup
        member = _get_team_membership(
            test_client,
            team["uuid"],
            manager_token,
            invitee_uuid,
        )
        assert member is not None
        test_client.delete(
            "/team/user",
            params={"userteamuuid": member["uuid"]},
            headers=_auth_headers(manager_token),
        )


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("regular_user", 403),
    ],
)
def test_remove_user_permissions(
    test_client,
    request,
    user_fixture,
    expected_status,
    manager_user,
    regular_user,
):
    manager_token = manager_user
    team = _create_team(test_client, manager_token)
    invitee_uuid = _get_user_uuid(test_client, regular_user)
    invite_payload = {
        "team_uuid": team["uuid"],
        "user_uuid": invitee_uuid,
        "team_role": "employee",
    }
    invite_response = test_client.post(
        "/team/user",
        json=invite_payload,
        headers=_auth_headers(manager_token),
    )
    assert invite_response.status_code == 200
    member = _get_team_membership(
        test_client,
        team["uuid"],
        manager_token,
        invitee_uuid,
    )
    assert member is not None

    token = request.getfixturevalue(user_fixture)
    response = test_client.delete(
        "/team/user",
        params={"userteamuuid": member["uuid"]},
        headers=_auth_headers(token),
    )
    assert response.status_code == expected_status

    if expected_status != 200:
        # cleanup by manager
        test_client.delete(
            "/team/user",
            params={"userteamuuid": member["uuid"]},
            headers=_auth_headers(manager_token),
        )


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("regular_user", 403),
    ],
)
def test_update_role_permissions(
    test_client,
    request,
    user_fixture,
    expected_status,
    manager_user,
    regular_user,
):
    manager_token = manager_user
    team = _create_team(test_client, manager_token)
    invitee_uuid = _get_user_uuid(test_client, regular_user)
    invite_payload = {
        "team_uuid": team["uuid"],
        "user_uuid": invitee_uuid,
        "team_role": "employee",
    }
    invite_response = test_client.post(
        "/team/user",
        json=invite_payload,
        headers=_auth_headers(manager_token),
    )
    assert invite_response.status_code == 200
    member = _get_team_membership(
        test_client,
        team["uuid"],
        manager_token,
        invitee_uuid,
    )
    assert member is not None

    token = request.getfixturevalue(user_fixture)
    payload = {
        "uuid": member["uuid"],
        "team_role": "manager",
    }
    response = test_client.patch(
        "/team/user",
        json=payload,
        headers=_auth_headers(token),
    )
    assert response.status_code == expected_status

    if expected_status == 200:
        body = response.json()
        assert body["uuid"] == member["uuid"]
        assert body["team_role"] == "manager"
    else:
        test_client.delete(
            "/team/user",
            params={"userteamuuid": member["uuid"]},
            headers=_auth_headers(manager_token),
        )


@pytest.mark.parametrize(
    "user_fixture",
    ["manager_user", "init_user", "regular_user"],
)
def test_get_team_permissions(
    test_client,
    request,
    user_fixture,
    manager_user,
):
    manager_token = manager_user
    team = _create_team(test_client, manager_token)

    token = request.getfixturevalue(user_fixture)
    response = test_client.get(
        "/team",
        params={"team_uuid": team["uuid"]},
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["uuid"] == team["uuid"]


def test_creator_added_to_team(test_client, manager_user):
    manager_token = manager_user
    team = _create_team(test_client, manager_token)
    response = test_client.get(
        "/team/my",
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200
    my_teams = response.json()
    assert any(
        item["team"]["uuid"] == team["uuid"]
        and item["team_role"] == "manager"
        for item in my_teams
    )
