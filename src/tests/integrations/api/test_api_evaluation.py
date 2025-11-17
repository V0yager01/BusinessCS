from datetime import date, datetime, timedelta, timezone
import uuid


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_team(test_client, manager_token: str) -> str:
    payload = {
        "name": f"Eval team {uuid.uuid4()}",
        "description": "Evaluation test team",
    }
    response = test_client.post(
        "/team",
        json=payload,
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200
    return response.json()["uuid"]


def _get_user_uuid(test_client, token: str) -> str:
    response = test_client.get(
        "/user/me",
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    return response.json()["uuid"]


def _add_user_to_team(test_client, manager_token: str, team_uuid: str, user_uuid: str):
    payload = {
        "team_uuid": team_uuid,
        "user_uuid": user_uuid,
        "team_role": "employee",
    }
    response = test_client.post(
        "/team/user",
        json=payload,
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200


def _get_team_membership_uuid(test_client, manager_token: str, team_uuid: str, target_uuid: str) -> str | None:
    response = test_client.get(
        "/team",
        params={"team_uuid": team_uuid},
        headers=_auth_headers(manager_token),
    )
    assert response.status_code == 200
    team_body = response.json()
    for team_user in team_body.get("teamuser", []):
        if team_user["user_relation"]["uuid"] == target_uuid:
            return team_user["uuid"]


def test_rate_task_flow(test_client, manager_user, regular_user):
    manager_token = manager_user
    performer_token = regular_user
    performer_uuid = _get_user_uuid(test_client, performer_token)

    team_uuid = _create_team(test_client, manager_token)
    _add_user_to_team(test_client, manager_token, team_uuid, performer_uuid)

    deadline = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    task_payload = {
        "title": "Task to evaluate",
        "description": "Task created for evaluation flow",
        "status": "waiting",
        "deadline": deadline,
        "team": team_uuid,
    }
    create_task = test_client.post(
        "/task",
        json=task_payload,
        headers=_auth_headers(manager_token),
    )
    assert create_task.status_code == 200
    task_body = create_task.json()
    task_uuid = task_body["uuid"]

    assign_payload = {"performer": performer_uuid}
    assign_response = test_client.patch(
        f"/task/{task_uuid}/performer",
        json=assign_payload,
        headers=_auth_headers(manager_token),
    )
    assert assign_response.status_code == 200

    rate_response = test_client.post(
        "/evaluation",
        params={"task_uuid": task_uuid, "rate": 4},
        headers=_auth_headers(manager_token),
    )
    assert rate_response.status_code == 200
    assert rate_response.json()["detail"] == "The task was rated"

    start_date = (date.today() - timedelta(days=1)).isoformat()
    end_date = (date.today() + timedelta(days=1)).isoformat()
    evaluations_response = test_client.get(
        "/evaluation/me",
        params={"star_date": start_date, "end_date": end_date},
        headers=_auth_headers(performer_token),
    )
    assert evaluations_response.status_code == 200
    evaluations = evaluations_response.json()
    assert isinstance(evaluations, list)
    assert any(item.get("task") == task_uuid for item in evaluations)

    test_client.delete(
        "/task",
        params={"task_uuid": task_uuid},
        headers=_auth_headers(manager_token),
    )
    member_uuid = _get_team_membership_uuid(
        test_client,
        manager_token,
        team_uuid,
        performer_uuid,
    )
    if member_uuid:
        test_client.delete(
            "/team/user",
            params={"userteamuuid": member_uuid},
            headers=_auth_headers(manager_token),
        )

