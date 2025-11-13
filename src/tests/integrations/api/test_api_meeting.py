from datetime import datetime, timedelta, timezone


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_creator_added_to_meeting_participants(test_client, manager_user):
    token = manager_user
    start_at = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
    payload = {
        "start_at": start_at,
        "meet_duration_hour": 1,
        "meet_duration_minutes": 0,
    }
    response = test_client.post(
        "/meeting",
        json=payload,
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    meeting = response.json()
    meeting_uuid = meeting["uuid"]

    my_meetings = test_client.get(
        "/meeting/mymeetings",
        headers=_auth_headers(token),
    )
    assert my_meetings.status_code == 200
    meetings_list = my_meetings.json()
    assert any(
        item.get("meeting_uuid") == meeting_uuid
        or item.get("meeting", {}).get("uuid") == meeting_uuid
        for item in meetings_list
    )

    test_client.delete(
        "/meeting",
        params={"meeting_uuid": meeting_uuid},
        headers=_auth_headers(token),
    )

