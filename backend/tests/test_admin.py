from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.models.users import UserOut, Enrollment, EnrollmentUpdate
from app.routers.admin import AdminRouter
from app.controllers.admin import AdminController
from app.services.admin import AdminService
from app.services.admin_mock import AdminMockService
from app.databases.dict import DictDB
from datetime import datetime, timedelta
from collections import deque
from app.models.admin import (
    AdminCreate,
    AdminLogin,
    LockStatusUpdate,
    RuleOut,
    RulePacket,
)
import pytest
import jwt


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

notification_channel: deque[RulePacket] = deque()

SECRET_KEY = "testing"


@pytest.fixture
def app():
    db = DictDB()
    service = AdminService(db, "testing-token", "testing-url", SECRET_KEY)
    mock_service = AdminMockService(service, users, enrollments, notification_channel)
    controller = AdminController(mock_service)
    router = AdminRouter(controller, SECRET_KEY)

    app = FastAPI()
    app.include_router(router.router)
    return app


def generate_test_token():
    payload = {"exp": datetime.utcnow() + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


VALID_HEADERS = {"Authorization": f"Bearer {generate_test_token()}"}


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)


###
#
# Auth
#
###
def test_hitting_endpoint_without_token(client: TestClient):
    res = client.get("/admins")
    assert res.status_code == 401


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

    res = client.get(f"/admins/{created['id']}", headers=VALID_HEADERS)
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
    res = client.post("/admins/login", json=adminLogin.model_dump())

    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_failure_invalid_password(client: TestClient):
    adminLogin = AdminLogin(email="alice@example.com", password="incorrectPassword")

    res = client.post("/admins/login", json=adminLogin.model_dump())
    assert res.status_code == 401
    assert res.json() == {"detail": "Invalid credentials"}


def test_login_failure_invalid_email_invalid_password(client: TestClient):
    adminLogin = AdminLogin(email="unknown@example.com", password="incorrectPassword")

    res = client.post("/admins/login", json=adminLogin.model_dump())
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


###
#
# Rules creation
#
###
base_rule = {
    "admin_name": "name",
    "title": "title",
    "description": "description",
    "effective_date": "2025-05-20T15:05:00Z",
    "applicable_conditions": ["cond1", "cond2"],
}


def test_create_rule(client: TestClient):
    res = client.get("/admins/rules", headers=VALID_HEADERS)
    assert res.status_code == 200

    data = res.json()
    assert len(data) == 0

    res = client.post(
        "/admins/rules",
        json=base_rule,
        headers=VALID_HEADERS,
    )
    assert res.status_code == 201

    res = client.get("/admins/rules", headers=VALID_HEADERS)
    assert res.status_code == 200

    data = res.json()
    assert len(data) == 1


def test_create_rule_with_same_title(client: TestClient):
    res = client.post(
        "/admins/rules",
        json=base_rule,
        headers=VALID_HEADERS,
    )
    assert res.status_code == 201

    data = {
        **base_rule,
        "description": "different description",
        "effective_date": "2026-06-21T16-06:01Z",
        "applicable_conditions": ["cond3", "cond4", "cond5"],
    }

    res = client.post(
        "/admins/rules",
        json=data,
        headers=VALID_HEADERS,
    )
    assert res.status_code == 409


###
#
# Rule Updating
#
###
base_update = {
    "admin_name": "name",
    "update": base_rule,
}


def test_rule_updating_exists(client: TestClient):
    res = client.post(
        "/admins/rules",
        json=base_rule,
        headers=VALID_HEADERS,
    )

    id = RuleOut(**res.json()).id
    new_title = "new title"

    res = client.patch(
        f"/admins/rules/{id}",
        json={**base_update, "update": {**base_rule, "title": new_title}},
        headers=VALID_HEADERS,
    )
    assert res.status_code == 200

    res = client.get(
        f"/admins/rules/{id}",
        headers=VALID_HEADERS,
    )
    assert res.status_code == 200

    rule = RuleOut(**res.json())
    assert rule.title == new_title


def test_rule_update_does_not_exist(client: TestClient):
    id = "some id"
    new_title = "new title"

    res = client.patch(
        f"/admins/rules/{id}",
        json={**base_update, "update": {**base_rule, "title": new_title}},
        headers=VALID_HEADERS,
    )
    assert res.status_code == 404


def test_rule_update_partial_data(client: TestClient):
    res = client.post(
        "/admins/rules",
        json=base_rule,
        headers=VALID_HEADERS,
    )

    id = RuleOut(**res.json()).id
    new_title = "new title"

    res = client.patch(
        f"/admins/rules/{id}",
        json={"admin_name": "name", "update": {"title": new_title}},
        headers=VALID_HEADERS,
    )
    assert res.status_code == 200

    res = client.get(
        f"/admins/rules/{id}",
        headers=VALID_HEADERS,
    )
    assert res.status_code == 200

    rule = RuleOut(**res.json())
    assert rule.title == new_title
    assert rule.description == base_rule["description"]
    assert rule.effective_date == base_rule["effective_date"]
    assert rule.applicable_conditions == base_rule["applicable_conditions"]


###
#
# Rule Notification
#
###
def test_sending_notifications_empty(client: TestClient):
    res = client.post("/admins/rules/notify", headers=VALID_HEADERS)
    assert res.status_code == 204
    assert len(notification_channel) == 1

    pkt = notification_channel.popleft()
    assert len(pkt.rules) == 0


def test_sending_notifications(client: TestClient):
    res = client.post(
        "/admins/rules",
        json=base_rule,
        headers=VALID_HEADERS,
    )
    assert res.status_code == 201

    res = client.post("/admins/rules/notify", headers=VALID_HEADERS)
    assert res.status_code == 204

    assert len(notification_channel) == 1

    pkt = notification_channel.popleft()
    assert len(pkt.rules) == 1
