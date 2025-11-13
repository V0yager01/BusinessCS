import uuid
from datetime import datetime, timedelta, timezone

import pytest


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_team_for_tasks(test_client, manager_token: str) -> str:
    payload = {
        "name": f"Task team {uuid.uuid4()}",
        "description": "Team for task tests",
    }
    response = test_client.post(
        "/team",
        json=payload,
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200
    return response.json()["uuid"]


@pytest.fixture()
def task_context(test_client, manager_user):
    manager_token = manager_user
    team_uuid = _create_team_for_tasks(test_client, manager_token)
    deadline = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    payload = {
        "title": "Initial task",
        "description": "Task for permissions tests",
        "status": "waiting",
        "deadline": deadline,
        "team": team_uuid,
    }
    response = test_client.post(
        "/task",
        json=payload,
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200
    body = response.json()
    task_uuid = body["uuid"]
    yield {
        "uuid": task_uuid,
        "team_uuid": team_uuid,
        "author_token": manager_token,
        "deadline": deadline,
    }
    test_client.delete(
        "/task",
        params={"task_uuid": task_uuid},
        headers=_auth_headers(manager_token),
    )


@pytest.mark.parametrize(
    "user_fixture, expected_status, new_title",
    [
        ("manager_user", 200, "Updated by manager"),
        ("init_user", 403, "Should not update"),
        ("regular_user", 403, "Should not update"),
    ],
)
def test_update_task_permissions(
    test_client,
    request,
    task_context,
    user_fixture,
    expected_status,
    new_title,
):
    token = request.getfixturevalue(user_fixture)
    payload = {
        "title": new_title,
        "description": "Updated description",
        "status": "in progress",
        "deadline": task_context["deadline"],
        "team": task_context["team_uuid"],
    }
    response = test_client.patch(
        f"/task/{task_context['uuid']}",
        json=payload,
        headers=_auth_headers(token),
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        assert body["uuid"] == task_context["uuid"]
        assert body["title"] == new_title


@pytest.mark.parametrize(
    "user_fixture",
    ["manager_user", "init_user", "regular_user"],
)
def test_comment_permissions(test_client, request, task_context, user_fixture):
    token = request.getfixturevalue(user_fixture)
    payload = {"text": f"Comment from {user_fixture}"}
    response = test_client.post(
        f"/task/{task_context['uuid']}/comment",
        json=payload,
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["text"] == payload["text"]


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("manager_user", 200),
        ("init_user", 403),
        ("regular_user", 403),
    ],
)
def test_delete_task_permissions(
    test_client,
    request,
    task_context,
    user_fixture,
    expected_status,
):
    token = request.getfixturevalue(user_fixture)
    response = test_client.delete(
        "/task",
        params={"task_uuid": task_context["uuid"]},
        headers=_auth_headers(token),
    )
    assert response.status_code == expected_status
