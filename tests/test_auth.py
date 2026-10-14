import uuid

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_signin_accepts_email_and_returns_token():
    email = f"{uuid.uuid4()}@example.com"
    response = client.post(
        "/api/auth/signin",
        json={"email": email, "password": "SecurePass123!"},
    )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["user"]["email"] == email
    assert payload["token"]


def test_signin_rejects_invalid_email_format():
    response = client.post(
        "/api/auth/signin",
        json={"email": "not-an-email", "password": "SecurePass123!"},
    )

    assert response.status_code == 400, response.text
    assert "valid email" in response.json()["detail"].lower()
