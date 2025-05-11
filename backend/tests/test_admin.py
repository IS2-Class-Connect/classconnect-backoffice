import pytest
from fastapi.testclient import TestClient
from app.models.admin import AdminCreate
from app.routers.admin import AdminRouter
from app.controllers.admin import AdminController
from app.services.admin import AdminService
from app.databases.dict import DictDB
from fastapi import FastAPI


@pytest.fixture
def app():
    db = DictDB()
    service = AdminService(db, "testing-token", "testing-url")
    controller = AdminController(service)
    router = AdminRouter(controller)

    app = FastAPI()
    app.include_router(router.router)
    return app


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)


def test_create_get_admin(client: TestClient):
    admin = AdminCreate(
        username="alice", email="alice@example.com", password="password"
    )

    res = client.post("/admins", json=admin.model_dump())
    created = res.json()

    assert res.status_code == 201
    assert created["username"] == admin.username
    assert created["email"] == admin.email

    res = client.get(f"/admins/{created['id']}")
    getted = res.json()

    assert res.status_code == 200
    assert getted["id"] == created["id"]
    assert getted["username"] == admin.username


def test_create_missing_fields(client: TestClient):
    # No username
    payload = {
        "email": "alice@example.com",
        "password": "12345678",
    }

    res = client.post("/admins", json=payload)
    assert res.status_code == 422

    # No email
    payload = {
        "username": "alice",
        "password": "12345678",
    }

    res = client.post("/admins", json=payload)
    assert res.status_code == 422

    # No password
    payload = {
        "username": "alice",
        "email": "alice@example.com",
    }

    res = client.post("/admins", json=payload)
    assert res.status_code == 422


def test_get_admin_not_found(client: TestClient):
    res = client.get("/admins/0")
    assert res.status_code == 404


def test_get_all_admins(client: TestClient):
    admins = [
        AdminCreate(username="bob", email="bob@example.com", password="password1"),
        AdminCreate(username="carol", email="carol@example.com", password="password2"),
    ]

    for admin in admins:
        client.post("/admins", json=admin.model_dump())

    res = client.get("/admins")
    getted = res.json()

    assert res.status_code == 200
    assert len(getted) == 2
    assert {admin["username"] for admin in getted} == {"bob", "carol"}


def test_duplicate_username_or_email(client: TestClient):
    admin = AdminCreate(username="dave", email="dave@example.com", password="password")
    client.post("/admins", json=admin.model_dump())

    same_username = AdminCreate(
        username="dave", email="different@example.com", password="password"
    )

    res = client.post("/admins", json=same_username.model_dump())
    assert res.status_code == 409
    assert res.json() == {"detail": "Username or email already exists"}

    same_email = AdminCreate(
        username="different", email="dave@example.com", password="password"
    )

    res = client.post("/admins", json=same_email.model_dump())
    assert res.status_code == 409
    assert res.json() == {"detail": "Username or email already exists"}


def test_delete_admin(client: TestClient):
    admin = AdminCreate(
        username="admin", email="admin@example.com", password="password"
    )
    res = client.post("/admins", json=admin.model_dump())
    created = res.json()
    id = created["id"]

    res = client.delete(f"/admins/{id}")
    assert res.status_code == 204

    res = client.get(f"/admins/{id}")
    assert res.status_code == 404
    assert res.json() == {"detail": "Admin not found"}


def test_delete_admin_not_found(client: TestClient):
    res = client.delete("/admins/0")
    assert res.status_code == 404
