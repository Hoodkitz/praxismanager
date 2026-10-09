import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    client.post("/api/auth/register", json={
        "email": "admin@praxis.de",
        "password": "secret123",
        "full_name": "Dr. Admin",
    })
    resp = client.post("/api/auth/login", json={
        "email": "admin@praxis.de",
        "password": "secret123",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# --- Health ---
def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# --- Auth ---
def test_register_user(client):
    resp = client.post("/api/auth/register", json={
        "email": "test@praxis.de",
        "password": "secret123",
        "full_name": "Dr. Test",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@praxis.de"
    assert data["full_name"] == "Dr. Test"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post("/api/auth/register", json={
        "email": "test@praxis.de",
        "password": "secret123",
        "full_name": "Dr. Test",
    })
    resp = client.post("/api/auth/register", json={
        "email": "test@praxis.de",
        "password": "secret123",
        "full_name": "Dr. Test 2",
    })
    assert resp.status_code == 400


def test_login_success(client):
    client.post("/api/auth/register", json={
        "email": "test@praxis.de",
        "password": "secret123",
        "full_name": "Dr. Test",
    })
    resp = client.post("/api/auth/login", json={
        "email": "test@praxis.de",
        "password": "secret123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "email": "test@praxis.de",
        "password": "secret123",
        "full_name": "Dr. Test",
    })
    resp = client.post("/api/auth/login", json={
        "email": "test@praxis.de",
        "password": "wrong",
    })
    assert resp.status_code == 401


def test_get_me(client, auth_headers):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "admin@praxis.de"


def test_get_me_no_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


# --- Patients ---
def test_create_patient(client):
    resp = client.post("/api/patients/", json={
        "first_name": "Max",
        "last_name": "Mustermann",
        "email": "max@example.de",
        "phone": "0123456789",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["first_name"] == "Max"
    assert data["last_name"] == "Mustermann"
    assert data["id"] is not None


def test_list_patients(client):
    client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"})
    client.post("/api/patients/", json={"first_name": "Erika", "last_name": "Musterfrau"})
    resp = client.get("/api/patients/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_patient(client):
    resp = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"})
    patient_id = resp.json()["id"]
    resp = client.get(f"/api/patients/{patient_id}")
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "Max"


def test_get_patient_not_found(client):
    resp = client.get("/api/patients/9999")
    assert resp.status_code == 404


def test_update_patient(client):
    resp = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"})
    patient_id = resp.json()["id"]
    resp = client.put(f"/api/patients/{patient_id}", json={"first_name": "Maximilian"})
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "Maximilian"


def test_delete_patient(client):
    resp = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"})
    patient_id = resp.json()["id"]
    resp = client.delete(f"/api/patients/{patient_id}")
    assert resp.status_code == 204
    resp = client.get(f"/api/patients/{patient_id}")
    assert resp.status_code == 404


# --- Appointments ---
def test_create_appointment(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    resp = client.post("/api/appointments/", json={
        "patient_id": patient["id"],
        "title": "Routineuntersuchung",
        "start_time": "2026-10-10T09:00:00",
        "end_time": "2026-10-10T09:30:00",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Routineuntersuchung"
    assert data["status"] == "scheduled"


def test_create_appointment_invalid_time(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    resp = client.post("/api/appointments/", json={
        "patient_id": patient["id"],
        "title": "Test",
        "start_time": "2026-10-10T10:00:00",
        "end_time": "2026-10-10T09:00:00",
    })
    assert resp.status_code == 400


def test_list_appointments(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    client.post("/api/appointments/", json={
        "patient_id": patient["id"],
        "title": "Termin 1",
        "start_time": "2026-10-10T09:00:00",
        "end_time": "2026-10-10T09:30:00",
    })
    resp = client.get("/api/appointments/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_update_appointment_status(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    appt = client.post("/api/appointments/", json={
        "patient_id": patient["id"],
        "title": "Termin",
        "start_time": "2026-10-10T09:00:00",
        "end_time": "2026-10-10T09:30:00",
    }).json()
    resp = client.put(f"/api/appointments/{appt['id']}", json={"status": "confirmed"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


def test_delete_appointment(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    appt = client.post("/api/appointments/", json={
        "patient_id": patient["id"],
        "title": "Termin",
        "start_time": "2026-10-10T09:00:00",
        "end_time": "2026-10-10T09:30:00",
    }).json()
    resp = client.delete(f"/api/appointments/{appt['id']}")
    assert resp.status_code == 204


# --- Invoices ---
def test_create_invoice(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    resp = client.post("/api/invoices/", json={
        "patient_id": patient["id"],
        "amount": 150.0,
        "description": "Behandlung",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["amount"] == 150.0
    assert data["invoice_number"].startswith("INV-")
    assert data["status"] == "draft"


def test_list_invoices(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    client.post("/api/invoices/", json={"patient_id": patient["id"], "amount": 100.0})
    resp = client.get("/api/invoices/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_update_invoice_status(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    inv = client.post("/api/invoices/", json={"patient_id": patient["id"], "amount": 100.0}).json()
    resp = client.put(f"/api/invoices/{inv['id']}", json={"status": "paid"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "paid"


def test_delete_invoice(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    inv = client.post("/api/invoices/", json={"patient_id": patient["id"], "amount": 100.0}).json()
    resp = client.delete(f"/api/invoices/{inv['id']}")
    assert resp.status_code == 204


# --- Dashboard ---
def test_dashboard_stats(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    client.post("/api/appointments/", json={
        "patient_id": patient["id"],
        "title": "Termin",
        "start_time": "2026-10-10T09:00:00",
        "end_time": "2026-10-10T09:30:00",
    })
    client.post("/api/invoices/", json={"patient_id": patient["id"], "amount": 200.0})
    resp = client.get("/api/dashboard/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_patients"] == 1
    assert data["total_appointments"] == 1
    assert data["total_invoices"] == 1
    assert data["revenue"] == 0.0  # invoice is draft, not paid


def test_dashboard_revenue(client):
    patient = client.post("/api/patients/", json={"first_name": "Max", "last_name": "Mustermann"}).json()
    inv = client.post("/api/invoices/", json={"patient_id": patient["id"], "amount": 200.0}).json()
    client.put(f"/api/invoices/{inv['id']}", json={"status": "paid"})
    resp = client.get("/api/dashboard/stats")
    assert resp.json()["revenue"] == 200.0
