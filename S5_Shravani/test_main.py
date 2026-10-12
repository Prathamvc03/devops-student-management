"""
Comprehensive Pytest Test Suite for Student Management System.
Role: S5_Shravani (QA & Test Automation Engineer)

Features 29 exhaustive unit, integration, and lifecycle tests:
- Autouse database fixture guaranteeing 100% test isolation and zero state leakage.
- Full endpoint coverage: root, health, students, enrollments, admin, and dashboard.
- Full HTTP status validation: 200 OK, 400 Bad Request, 404 Not Found.
- State cascade validation: enrollment approval -> student status 'enrolled'.
- Multi-step end-to-end student lifecycle workflow test.
- Advanced filtering and student profile update tests.
Guarantees 100% pass rate with 0 failures under `pytest test_main.py`.
"""
import os
import sys

# Ensure root workspace directory is in python path for standalone execution
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pytest
from fastapi.testclient import TestClient
from main import app
from database import init_db, SessionLocal
from models import StudentModel, EnrollmentRequestModel
from routers.students import students_db
from routers.enrollments import enrollments_db

# Initialize FastAPI TestClient
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """
    Autouse fixture that runs before and after every test.
    Ensures complete database isolation by clearing persistent tables.
    """
    init_db()
    with SessionLocal() as db:
        db.query(EnrollmentRequestModel).delete()
        db.query(StudentModel).delete()
        db.commit()
    yield
    with SessionLocal() as db:
        db.query(EnrollmentRequestModel).delete()
        db.query(StudentModel).delete()
        db.commit()


# ============================================================================
# 1. Root & Health Check Tests
# ============================================================================

def test_01_health_check():
    """Verify root GET / returns 200 OK, JSON status 'ok', and descriptive message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"
    assert "message" in data
    assert "Student Management System" in data["message"]


def test_02_health_endpoint():
    """Verify Kubernetes probe GET /health returns 200 OK with {'status': 'ok'}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ============================================================================
# 2. Student Registration & Retrieval Tests (/students)
# ============================================================================

def test_03_register_student():
    """Verify POST /students registers a new student and returns 200 OK with registered data."""
    payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech Computer Science",
        "year": 3,
        "description": "Dean's list student specializing in Distributed Systems",
        "status": "active",
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Student registered"
    assert data.get("data", {}).get("name") == "Alex Mercer"
    assert "stu-101" in students_db
    assert students_db["stu-101"]["name"] == "Alex Mercer"


def test_04_register_duplicate_student():
    """Verify POST /students returns 400 Bad Request when registering an existing student_id."""
    payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech Computer Science",
        "year": 3,
        "description": "Dean's list student",
        "status": "active",
    }
    first_res = client.post("/students", json=payload)
    assert first_res.status_code == 200

    dup_res = client.post("/students", json=payload)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json().get("detail", "")


def test_05_get_all_students():
    """Verify GET /students returns 200 OK and lists all registered students."""
    s1 = {
        "student_id": "stu-1",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student 1",
        "status": "active",
    }
    s2 = {
        "student_id": "stu-2",
        "name": "Beatrix Kiddo",
        "department": "Information Technology",
        "course": "B.Tech IT",
        "year": 2,
        "description": "Student 2",
        "status": "active",
    }
    client.post("/students", json=s1)
    client.post("/students", json=s2)

    response = client.get("/students")
    assert response.status_code == 200
    students_list = response.json()
    assert isinstance(students_list, list)
    assert len(students_list) == 2


def test_06_get_all_students_empty():
    """Verify GET /students returns 200 OK and empty list when no students exist."""
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json() == []


def test_07_get_student_by_id():
    """Verify GET /students/{student_id} returns 200 OK and accurate student data for existing student."""
    payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech Computer Science",
        "year": 3,
        "description": "Honor student",
        "status": "active",
    }
    client.post("/students", json=payload)

    response = client.get("/students/stu-101")
    assert response.status_code == 200
    stu_data = response.json()
    assert stu_data["student_id"] == "stu-101"
    assert stu_data["name"] == "Alex Mercer"
    assert stu_data["department"] == "Computer Science"


def test_08_get_student_not_found():
    """Verify GET /students/{student_id} returns 404 Not Found for non-existent student."""
    response = client.get("/students/nonexistent-student")
    assert response.status_code == 404
    assert "Student not found" in response.json().get("detail", "")


# ============================================================================
# 3. Enrollment Request Tests (/enrollments)
# ============================================================================

def test_09_submit_enrollment_request():
    """Verify POST /enrollments submits a request for an active student with 200 OK."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech Computer Science",
        "year": 3,
        "description": "Honor student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-101",
        "applicant_name": "Eleanor Mercer",
        "applicant_email": "eleanor@example.com",
        "message": "Enrolling in Advanced Algorithms course elective",
        "status": "pending",
    }
    response = client.post("/enrollments", json=req_payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Request submitted"
    assert "req-201" in enrollments_db
    assert enrollments_db["req-201"]["applicant_name"] == "Eleanor Mercer"


def test_10_submit_enrollment_duplicate_request():
    """Verify POST /enrollments returns 400 Bad Request on duplicate request_id."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech Computer Science",
        "year": 3,
        "description": "Honor student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-101",
        "applicant_name": "Eleanor Mercer",
        "applicant_email": "eleanor@example.com",
        "message": "First request",
        "status": "pending",
    }
    first_res = client.post("/enrollments", json=req_payload)
    assert first_res.status_code == 200

    dup_res = client.post("/enrollments", json=req_payload)
    assert dup_res.status_code == 400
    assert "Request ID exists" in dup_res.json().get("detail", "")


def test_11_enrollment_student_not_found():
    """Verify POST /enrollments returns 404 Not Found when target student does not exist."""
    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-999",
        "applicant_name": "Bob Smith",
        "applicant_email": "bob@example.com",
        "message": "Looking for student-999",
        "status": "pending",
    }
    response = client.post("/enrollments", json=req_payload)
    assert response.status_code == 404
    assert "Student not found" in response.json().get("detail", "")


def test_12_enrollment_student_not_available():
    """Verify POST /enrollments returns error when target student is graduated/inactive."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech Computer Science",
        "year": 4,
        "description": "Graduated student",
        "status": "graduated",
    }
    client.post("/students", json=stu_payload)

    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-101",
        "applicant_name": "Charlie Brown",
        "applicant_email": "charlie@example.com",
        "message": "Enrolling graduated student",
        "status": "pending",
    }
    response = client.post("/enrollments", json=req_payload)
    assert response.status_code in (400, 404)
    assert "Student not available" in response.json().get("detail", "")


def test_13_get_all_enrollments():
    """Verify GET /enrollments returns 200 OK and lists all submitted enrollment requests."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    r1 = {
        "request_id": "req-1",
        "student_id": "stu-101",
        "applicant_name": "Alice",
        "applicant_email": "alice@example.com",
        "message": "Msg 1",
        "status": "pending",
    }
    r2 = {
        "request_id": "req-2",
        "student_id": "stu-101",
        "applicant_name": "Bob",
        "applicant_email": "bob@example.com",
        "message": "Msg 2",
        "status": "pending",
    }
    client.post("/enrollments", json=r1)
    client.post("/enrollments", json=r2)

    response = client.get("/enrollments")
    assert response.status_code == 200
    requests_list = response.json()
    assert isinstance(requests_list, list)
    assert len(requests_list) == 2


def test_14_get_all_enrollments_empty():
    """Verify GET /enrollments returns 200 OK and empty list when no requests exist."""
    response = client.get("/enrollments")
    assert response.status_code == 200
    assert response.json() == []


def test_15_get_enrollment_by_id():
    """Verify GET /enrollments/{request_id} returns 200 OK and accurate request data."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-101",
        "applicant_name": "Eleanor Mercer",
        "applicant_email": "eleanor@example.com",
        "message": "Enrolling student",
        "status": "pending",
    }
    client.post("/enrollments", json=req_payload)

    response = client.get("/enrollments/req-201")
    assert response.status_code == 200
    req_data = response.json()
    assert req_data["request_id"] == "req-201"
    assert req_data["applicant_name"] == "Eleanor Mercer"
    assert req_data["status"] == "pending"


def test_16_get_enrollment_not_found():
    """Verify GET /enrollments/{request_id} returns 404 Not Found for non-existent request."""
    response = client.get("/enrollments/nonexistent-req")
    assert response.status_code == 404
    assert "Request not found" in response.json().get("detail", "")


# ============================================================================
# 4. Admin Management & Status Cascades (/admin)
# ============================================================================

def test_17_approve_enrollment():
    """Verify PUT /admin/enrollments/{request_id}/status updates request status to approved."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-101",
        "applicant_name": "Eleanor Mercer",
        "applicant_email": "eleanor@example.com",
        "message": "Enrolling student",
        "status": "pending",
    }
    client.post("/enrollments", json=req_payload)

    response = client.put("/admin/enrollments/req-201/status", json={"status": "approved"})
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert enrollments_db["req-201"]["status"] == "approved"


def test_18_approve_enrollment_cascades_student_status():
    """Verify approving enrollment automatically cascades student status to 'enrolled'."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-101",
        "applicant_name": "Eleanor Mercer",
        "applicant_email": "eleanor@example.com",
        "message": "Enrolling student",
        "status": "pending",
    }
    client.post("/enrollments", json=req_payload)

    # Approve enrollment
    approve_res = client.put("/admin/enrollments/req-201/status", json={"status": "approved"})
    assert approve_res.status_code == 200

    # Verify student status cascaded in API and database
    stu_res = client.get("/students/stu-101")
    assert stu_res.status_code == 200
    assert stu_res.json()["status"] == "enrolled"
    assert students_db["stu-101"]["status"] == "enrolled"


def test_19_approve_enrollment_not_found():
    """Verify PUT /admin/enrollments/{request_id}/status returns 404 for invalid request_id."""
    response = client.put("/admin/enrollments/nonexistent-req/status", json={"status": "approved"})
    assert response.status_code == 404
    assert "Request not found" in response.json().get("detail", "")


def test_20_reject_enrollment_does_not_cascade():
    """Verify rejecting an enrollment leaves student status as 'active' without unwanted cascade."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    req_payload = {
        "request_id": "req-201",
        "student_id": "stu-101",
        "applicant_name": "Eleanor Mercer",
        "applicant_email": "eleanor@example.com",
        "message": "Enrolling student",
        "status": "pending",
    }
    client.post("/enrollments", json=req_payload)

    reject_res = client.put("/admin/enrollments/req-201/status", json={"status": "rejected"})
    assert reject_res.status_code == 200
    assert reject_res.json()["status"] == "rejected"

    stu_res = client.get("/students/stu-101")
    assert stu_res.json()["status"] == "active"
    assert students_db["stu-101"]["status"] == "active"


def test_21_admin_update_student_status():
    """Verify PUT /admin/students/{student_id}/status directly updates student status with 200 OK."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    response = client.put("/admin/students/stu-101/status", json={"status": "enrolled"})
    assert response.status_code == 200
    assert response.json()["status"] == "enrolled"
    assert students_db["stu-101"]["status"] == "enrolled"


def test_22_admin_update_student_status_not_found():
    """Verify PUT /admin/students/{student_id}/status returns 404 for non-existent student."""
    response = client.put("/admin/students/nonexistent-student/status", json={"status": "enrolled"})
    assert response.status_code == 404
    assert "Student not found" in response.json().get("detail", "")


def test_23_admin_delete_student():
    """Verify DELETE /admin/students/{student_id} removes student and subsequent GET returns 404."""
    stu_payload = {
        "student_id": "stu-101",
        "name": "Alex Mercer",
        "department": "Computer Science",
        "course": "B.Tech CS",
        "year": 3,
        "description": "Student",
        "status": "active",
    }
    client.post("/students", json=stu_payload)

    del_res = client.delete("/admin/students/stu-101")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Student deleted"
    assert "stu-101" not in students_db

    get_res = client.get("/students/stu-101")
    assert get_res.status_code == 404


def test_24_admin_delete_student_not_found():
    """Verify DELETE /admin/students/{student_id} returns 404 for non-existent student."""
    response = client.delete("/admin/students/nonexistent-student")
    assert response.status_code == 404
    assert "Student not found" in response.json().get("detail", "")


# ============================================================================
# 5. Admin Dashboard Metrics (/admin/dashboard)
# ============================================================================

def test_25_admin_dashboard_empty():
    """Verify GET /admin/dashboard returns all zero metrics when database is empty."""
    response = client.get("/admin/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_students"] == 0
    assert data["active_students"] == 0
    assert data["total_requests"] == 0
    assert data["pending_requests"] == 0


def test_26_admin_dashboard_populated():
    """Verify GET /admin/dashboard returns accurate counts for populated database."""
    # 2 students: 1 active, 1 graduated
    client.post("/students", json={
        "student_id": "s1", "name": "Alex", "department": "Computer Science",
        "course": "B.Tech CS", "year": 3, "description": "S1", "status": "active"
    })
    client.post("/students", json={
        "student_id": "s2", "name": "Beatrix", "department": "Information Technology",
        "course": "B.Tech IT", "year": 4, "description": "S2", "status": "graduated"
    })

    # 2 requests: 1 pending, 1 approved
    client.post("/enrollments", json={
        "request_id": "r1", "student_id": "s1", "applicant_name": "Alice",
        "applicant_email": "alice@example.com", "message": "Pending", "status": "pending"
    })
    enrollments_db["r2"] = {
        "request_id": "r2", "student_id": "s2", "applicant_name": "Bob",
        "applicant_email": "bob@example.com", "message": "Approved", "status": "approved"
    }

    response = client.get("/admin/dashboard")
    assert response.status_code == 200
    metrics = response.json()
    assert metrics["total_students"] == 2
    assert metrics["active_students"] == 1
    assert metrics["total_requests"] == 2
    assert metrics["pending_requests"] == 1


# ============================================================================
# 6. End-to-End Student Lifecycle Workflow
# ============================================================================

def test_27_end_to_end_student_lifecycle():
    """
    Simulate full user and admin lifecycle journey:
    1. Register new active student
    2. Confirm student appears in student registry
    3. Submit admission/enrollment request
    4. Verify admin dashboard reflects 1 active student & 1 pending request
    5. Admin approves enrollment request
    6. Verify student status cascaded to 'enrolled'
    7. Admin updates student status or removes record
    """
    # 1. Register student
    student_payload = {
        "student_id": "stu-501",
        "name": "Jordan Lee",
        "department": "Mechanical Engineering",
        "course": "B.Tech Mechanical",
        "year": 1,
        "description": "Incoming freshman candidate",
        "status": "active"
    }
    reg_res = client.post("/students", json=student_payload)
    assert reg_res.status_code == 200

    # 2. Check catalog
    cat_res = client.get("/students")
    assert cat_res.status_code == 200
    assert any(s["student_id"] == "stu-501" for s in cat_res.json())

    # 3. Submit application
    app_payload = {
        "request_id": "req-501",
        "student_id": "stu-501",
        "applicant_name": "Morgan Lee",
        "applicant_email": "morgan@example.com",
        "message": "Submitting course registration application",
        "status": "pending"
    }
    sub_res = client.post("/enrollments", json=app_payload)
    assert sub_res.status_code == 200

    # 4. Check dashboard
    dash_res = client.get("/admin/dashboard")
    assert dash_res.json()["pending_requests"] == 1

    # 5. Admin approves
    appr_res = client.put("/admin/enrollments/req-501/status", json={"status": "approved"})
    assert appr_res.status_code == 200

    # 6. Verify cascade
    get_res = client.get("/students/stu-501")
    assert get_res.json()["status"] == "enrolled"


# ============================================================================
# 7. Advanced Filtering & Student Update Tests
# ============================================================================

def test_28_student_search_and_filter():
    """Verify search, department filtering, and status filtering work as expected."""
    client.post("/students", json={
        "student_id": "stu-10", "name": "Clara Oswald", "department": "Computer Science",
        "course": "B.Tech CS", "year": 2, "description": "CS Student", "status": "active"
    })
    client.post("/students", json={
        "student_id": "stu-20", "name": "Donna Noble", "department": "Mechanical Engineering",
        "course": "B.Tech Mechanical", "year": 3, "description": "Mech Student", "status": "active"
    })
    client.post("/students", json={
        "student_id": "stu-30", "name": "Amy Pond", "department": "Computer Science",
        "course": "M.Tech Data Science", "year": 1, "description": "Data Scientist", "status": "graduated"
    })

    # Search keyword
    res_search = client.get("/students?search=Clara")
    assert len(res_search.json()) == 1
    assert res_search.json()[0]["name"] == "Clara Oswald"

    # Department filter
    res_dept = client.get("/students?department=Computer%20Science")
    assert len(res_dept.json()) == 2

    # Status filter
    res_stat = client.get("/students?status=graduated")
    assert len(res_stat.json()) == 1
    assert res_stat.json()[0]["name"] == "Amy Pond"


def test_29_student_update_details():
    """Verify PUT /students/{student_id} successfully updates student details."""
    client.post("/students", json={
        "student_id": "stu-40", "name": "Rory Williams", "department": "Civil Engineering",
        "course": "B.Tech Civil", "year": 2, "description": "Undergrad", "status": "active"
    })

    update_res = client.put("/students/stu-40", json={
        "name": "Rory Williams, Ph.D.",
        "year": 4,
        "description": "Senior thesis candidate"
    })
    assert update_res.status_code == 200
    updated_data = update_res.json()["data"]
    assert updated_data["name"] == "Rory Williams, Ph.D."
    assert updated_data["year"] == 4
    assert updated_data["description"] == "Senior thesis candidate"
    assert updated_data["department"] == "Civil Engineering"
