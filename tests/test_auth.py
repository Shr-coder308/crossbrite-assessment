def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_login_success(client):
    response = client.post(
        "/auth/login",
        params={
            "email": "teacher2@example.com",
            "password": "Teacher@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    response = client.post(
        "/auth/login",
        params={
            "email": "teacher2@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401