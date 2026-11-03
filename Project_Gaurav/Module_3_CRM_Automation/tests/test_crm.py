import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("CRM_API_KEY", "test-secret-key")

    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(
        app,
        headers={"X-API-Key": "test-secret-key"}
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_key_required(client):
    unauthenticated_client = TestClient(app)

    response = unauthenticated_client.get("/api/leads")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key"


def test_create_list_update_delete_lead(client):
    payload = {
        "name": "Asha Sharma",
        "email": "asha@example.com",
        "company": "ABC Ltd"
    }

    created = client.post("/api/leads", json=payload)

    assert created.status_code == 201

    lead_id = created.json()["id"]

    assert client.get("/api/leads").json()[0]["name"] == "Asha Sharma"

    updated = client.patch(
        f"/api/leads/{lead_id}",
        json={"status": "Interested"}
    )

    assert updated.status_code == 200
    assert updated.json()["status"] == "Interested"

    assert client.delete(f"/api/leads/{lead_id}").status_code == 204


def test_follow_up_and_interaction(client):
    lead = client.post(
        "/api/leads",
        json={"name": "Test Lead"}
    ).json()

    lead_id = lead["id"]

    follow = client.post(
        f"/api/leads/{lead_id}/follow-ups",
        json={
            "due_date": "2026-11-10",
            "description": "Call the prospect"
        },
    )

    assert follow.status_code == 201
    assert follow.json()["status"] == "Pending"

    interaction = client.post(
        f"/api/leads/{lead_id}/interactions",
        json={
            "interaction_type": "Call",
            "details": "Discussed requirements"
        },
    )

    assert interaction.status_code == 201
    assert interaction.json()["interaction_type"] == "Call"


def test_invalid_lead_status(client):
    response = client.post(
        "/api/leads",
        json={"name": "Test", "status": "Unknown"}
    )

    assert response.status_code == 422


def test_empty_lead_update(client):
    created = client.post(
        "/api/leads",
        json={"name": "Soni Maurya"}
    )

    assert created.status_code == 201

    lead_id = created.json()["id"]

    response = client.patch(
        f"/api/leads/{lead_id}",
        json={}
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "At least one field must be provided"