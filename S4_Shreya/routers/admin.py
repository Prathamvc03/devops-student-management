"""
Admin Management Router.
Handles student record deletion, student status updates, enrollment approvals with cascade,
and dashboard metrics via persistent database.
Author: Shreya (S4_Shreya)
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import StatusUpdate, StudentModel, EnrollmentRequestModel
from routers.students import students_db
from routers.enrollments import enrollments_db

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.put("/enrollments/{request_id}/status")
def update_enrollment_status(request_id: str, update: StatusUpdate, db: Session = Depends(get_db)):
    """
    Update enrollment request status (e.g., 'approved', 'rejected').
    If approved, cascades student status to 'enrolled'.
    Returns 404 if request not found.
    """
    req = db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    req.status = update.status

    if update.status == "approved":
        student = db.query(StudentModel).filter(StudentModel.student_id == req.student_id).first()
        if student:
            student.status = "enrolled"

    db.commit()
    db.refresh(req)
    return req.to_dict()


@router.put("/students/{student_id}/status")
def update_student_status(student_id: str, update: StatusUpdate, db: Session = Depends(get_db)):
    """
    Update a student's status directly (e.g., 'active', 'enrolled', 'graduated', 'inactive').
    Returns 404 if student not found.
    """
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.status = update.status
    db.commit()
    db.refresh(student)
    return student.to_dict()


@router.delete("/students/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    """
    Remove a student record from the database.
    Cascades deletion to any associated enrollment requests.
    Returns 404 if student not found.
    """
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    deleted_data = student.to_dict()
    db.delete(student)
    db.commit()
    return {"message": "Student deleted", "student_id": student_id, "student": deleted_data}


@router.get("/dashboard")
@router.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    """
    Return administrative summary dashboard metrics from database.
    """
    total_students = db.query(StudentModel).count()
    active_students = db.query(StudentModel).filter(StudentModel.status.in_(["active", "enrolled"])).count()
    total_requests = db.query(EnrollmentRequestModel).count()
    pending_requests = db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.status == "pending").count()

    # Department breakdown
    all_students = db.query(StudentModel).all()
    departments = {}
    for s in all_students:
        dept = s.department or "General"
        departments[dept] = departments.get(dept, 0) + 1

    return {
        "total_students": total_students,
        "available_students": active_students,
        "active_students": active_students,
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "department_stats": departments
    }
