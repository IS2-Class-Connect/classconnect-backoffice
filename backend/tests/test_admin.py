import pytest
from fastapi.testclient import TestClient
from app.models.admin import AdminCreate, AdminLogin, LockStatusUpdate
from app.models.users import UserOut, Enrollment, EnrollmentUpdate
from app.routers.admin import AdminRouter
from app.controllers.admin import AdminController
from app.services.admin import AdminService
from app.services.admin_mock import AdminMockService
from app.databases.dict import DictDB
from fastapi import FastAPI

users: dict[str, UserOut] = {
    "1": UserOut(
        **{
            "uuid": "1",
            "email": "juan@example.com",
            "name": "juan",
            "urlProfilePhoto": "https://example.com/photo1.jpg",
            "description": "Usuario activo",
            "createdAt": "2025-05-20T15:00:00Z",
            "accountLockedByAdmins": False,
        }
    ),
    "2": UserOut(
        **{
            "uuid": "2",
            "email": "maria@example.com",
            "name": "maria",
            "urlProfilePhoto": "https://example.com/photo2.jpg",
            "description": "Usuario activo",
            "createdAt": "2025-05-20T15:05:00Z",
            "accountLockedByAdmins": False,
        }
    ),
}

enrollments: dict[str, dict[str, Enrollment]] = {
    "1": {
        "101": Enrollment(
            **{
                "role": "student",
                "userId": "user1",
                "course": {"id": 101, "title": "Matemáticas Básicas"},
            }
        ),
    },
    "2": {
        "102": Enrollment(
            **{
                "role": "teacher",
                "userId": "user2",
                "course": {"id": 102, "title": "Historia Universal"},
            }
        ),
    },
}

SECRET_KEY = "testing"


@pytest.fixture
def app():
    db = DictDB()
    service = AdminService(db, "testing-token", "testing-url", SECRET_KEY)
    mock_service = AdminMockService(service, users, enrollments)
    controller = AdminController(mock_service)
    router = AdminRouter(controller)

    app = FastAPI()
    app.include_router(router.router)
    return app


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)


VALID_HEADERS = {"Authorization": f"Bearer {SECRET_KEY}"}


###
#
# Admin Creation
#
###
def test_create_get_admin(client: TestClient):
    admin = AdminCreate(
        username="alice", email="alice@example.com", password="password"
    )

    res = client.post("/admins", json=admin.model_dump(), headers=VALID_HEADERS)
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

    res = client.post("/admins", json=payload, headers=VALID_HEADERS)
    assert res.status_code == 422

    # No email
    payload = {
        "username": "alice",
        "password": "12345678",
    }

    res = client.post("/admins", json=payload, headers=VALID_HEADERS)
    assert res.status_code == 422

    # No password
    payload = {
        "username": "alice",
        "email": "alice@example.com",
    }

    res = client.post("/admins", json=payload, headers=VALID_HEADERS)
    assert res.status_code == 422


def test_duplicate_username_or_email(client: TestClient):
    admin = AdminCreate(username="dave", email="dave@example.com", password="password")
    client.post("/admins", json=admin.model_dump(), headers=VALID_HEADERS)

    same_username = AdminCreate(
        username="dave", email="different@example.com", password="password"
    )

    res = client.post("/admins", json=same_username.model_dump(), headers=VALID_HEADERS)
    assert res.status_code == 409
    assert res.json() == {"detail": "Username or email already exists"}

    same_email = AdminCreate(
        username="different", email="dave@example.com", password="password"
    )

    res = client.post("/admins", json=same_email.model_dump(), headers=VALID_HEADERS)
    assert res.status_code == 409
    assert res.json() == {"detail": "Username or email already exists"}


###
#
# Admin Retrieval
#
###
def test_get_admin_not_found(client: TestClient):
    res = client.get("/admins/0", headers=VALID_HEADERS)
    assert res.status_code == 404


def test_get_all_admins(client: TestClient):
    admins = [
        AdminCreate(username="bob", email="bob@example.com", password="password1"),
        AdminCreate(username="carol", email="carol@example.com", password="password2"),
    ]

    for admin in admins:
        client.post("/admins", json=admin.model_dump(), headers=VALID_HEADERS)

    res = client.get("/admins", headers=VALID_HEADERS)
    getted = res.json()

    assert res.status_code == 200
    assert len(getted) == 2
    assert {admin["username"] for admin in getted} == {"bob", "carol"}


###
#
# Admin Deletion
#
###
def test_delete_admin(client: TestClient):
    admin = AdminCreate(
        username="admin", email="admin@example.com", password="password"
    )
    res = client.post("/admins", json=admin.model_dump(), headers=VALID_HEADERS)
    created = res.json()
    id = created["id"]

    res = client.delete(f"/admins/{id}", headers=VALID_HEADERS)
    assert res.status_code == 204

    res = client.get(f"/admins/{id}", headers=VALID_HEADERS)
    assert res.status_code == 404
    assert res.json() == {"detail": "Admin not found"}


def test_delete_admin_not_found(client: TestClient):
    res = client.delete("/admins/0", headers=VALID_HEADERS)
    assert res.status_code == 404


###
#
# Admin Login
#
###
def test_login(client: TestClient):
    admin = AdminCreate(
        username="alice", email="alice@example.com", password="password"
    )

    res = client.post("/admins", json=admin.model_dump(), headers=VALID_HEADERS)
    created = res.json()

    assert res.status_code == 201
    assert created["username"] == admin.username
    assert created["email"] == admin.email

    adminLogin = AdminLogin(email="alice@example.com", password="password")
    res = client.post(
        "/admins/login", json=adminLogin.model_dump(), headers=VALID_HEADERS
    )

    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_failure_invalid_password(client: TestClient):
    adminLogin = AdminLogin(email="alice@example.com", password="incorrectPassword")

    res = client.post(
        "/admins/login", json=adminLogin.model_dump(), headers=VALID_HEADERS
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Invalid credentials"}


def test_login_failure_invalid_email_invalid_password(client: TestClient):
    adminLogin = AdminLogin(email="unknown@example.com", password="incorrectPassword")

    res = client.post(
        "/admins/login", json=adminLogin.model_dump(), headers=VALID_HEADERS
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Invalid credentials"}


###
#
# User Retrieval
#
###
def test_get_all_users(client: TestClient):
    response = client.get("/admins/users", headers=VALID_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "juan"
    assert data[1]["email"] == "maria@example.com"


###
#
# User Lock Status
#
###
def test_lock_status(client: TestClient):
    uuid = "1"

    assert not users[uuid].accountLockedByAdmins

    data = LockStatusUpdate(locked=True)
    res = client.patch(
        f"/admins/users/{uuid}/lock-status",
        json=data.model_dump(),
        headers=VALID_HEADERS,
    )

    assert res.status_code == 200
    assert users[uuid].accountLockedByAdmins

    # unwind global state
    users[uuid].accountLockedByAdmins = False


def test_lock_status_invalid_id(client: TestClient):
    uuid = "123456789"

    data = LockStatusUpdate(locked=True)
    res = client.patch(
        f"/admins/users/{uuid}/lock-status",
        json=data.model_dump(),
        headers=VALID_HEADERS,
    )

    assert res.status_code == 404


###
#
# User Enrollment Retrieval
#
###
def test_get_all_users_enrollment(client: TestClient):
    response = client.get("/admins/courses/enrollments", headers=VALID_HEADERS)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["role"] == "student"
    assert data[0]["userId"] == "user1"
    assert data[0]["course"]["title"] == "Matemáticas Básicas"

    assert data[1]["role"] == "teacher"
    assert data[1]["course"]["id"] == 102


###
#
# User Enrollment Update
#
###
def test_update_user_enrollment(client: TestClient):
    enrollment_uuid = "101"
    user_uuid = "1"
    data = EnrollmentUpdate(role="teacher")

    assert enrollments[user_uuid][enrollment_uuid].role == "student"

    res = client.patch(
        f"/admins/courses/{enrollment_uuid}/enrollments/{user_uuid}",
        json=data.model_dump(),
        headers=VALID_HEADERS,
    )

    assert res.status_code == 200
    assert enrollments[user_uuid][enrollment_uuid].role == "teacher"

    # unwind global state
    enrollments[user_uuid][enrollment_uuid].role = "student"
