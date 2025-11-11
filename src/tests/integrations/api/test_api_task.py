import pytest

from src.task.router import router


@pytest.fixture()
def create_task(init_user, test_client):
    token = init_user
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "string",
        "description": "string",
        "status": "waiting",
        "deadline": "2025-11-10T23:04:58.395Z"
        }
    response = test_client.post("/task", json=data, headers=headers)
    assert response.status_code == 200
    body = response.json()
    uuid = body.get("uuid")
    assert uuid is not None
    yield uuid
    test_client.delete("/task", params={"task_uuid": uuid}, headers=headers)


@pytest.mark.parametrize(
    "user_fixture, expected_status, expected_title",
    [
        ("init_user", 200, "Updated by init_user"),
        ("regular_user", 403, None),
        ("manager_user", 403, None),
    ],
)
def test_update_task_permissions(test_client, request, create_task, user_fixture, expected_status, expected_title):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": expected_title,
        "description": "string",
        "status": "waiting",
        "deadline": "2025-11-10T23:04:58.395Z"
        }
    response = test_client.patch(f"/task/{create_task}", json=data, headers=headers)
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        assert body["uuid"] == create_task
        assert body["title"] == expected_title


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("init_user", 200),
        ("regular_user", 200),
        ("manager_user", 200),
    ],
)
def test_comment_permissions(test_client, request, create_task, user_fixture, expected_status):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"text": f"Comment"}
    response = test_client.post(f"/task/{create_task}/comment", json=payload, headers=headers)
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        assert body["text"] == payload["text"]

@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("init_user", 200),
        ("regular_user", 403),
        ("manager_user", 403),
    ],
)
def test_delete_task_permissions(test_client, request, create_task, user_fixture, expected_status):
    token = request.getfixturevalue(user_fixture)
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.delete("/task", params={"task_uuid": create_task}, headers=headers)
    assert response.status_code == expected_status
