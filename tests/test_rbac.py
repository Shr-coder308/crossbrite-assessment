def get_token(client, email, password):
    response = client.post(
        "/auth/login",
        params={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_teacher_can_access_own_sessions(client):
    token = get_token(
        client,
        "teacher2@example.com",
        "Teacher@123",
    )

    response = client.get(
        "/sessions/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200


def test_parent_cannot_create_session(client):
    token = get_token(
        client,
        "parent@example.com",
        "Parent@123",
    )

    response = client.post(
        "/sessions/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Unauthorized Session",
            "description": "This should not be created",
            "scheduled_at": "2026-09-20T10:00:00",
        },
    )

    assert response.status_code == 403


def test_parent_can_access_own_child_evaluations(client):
    token = get_token(
        client,
        "parent@example.com",
        "Parent@123",
    )

    response = client.get(
        "/evaluations/my-child",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    evaluations = response.json()

    assert len(evaluations) >= 1
    assert evaluations[0]["student_id"] == 9


def test_parent_cannot_trigger_evaluation(client):
    token = get_token(
        client,
        "parent@example.com",
        "Parent@123",
    )

    response = client.post(
        "/evaluations/trigger/1",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "student_id": 9,
        },
    )

    assert response.status_code == 403