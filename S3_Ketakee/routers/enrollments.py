"""
Enrollment Request Router.
Handles student enrollment and admission request submissions and retrievals backed by persistent database.
Author: Ketakee (S3_Ketakee)
"""
import collections.abc
from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, SessionLocal, init_db
from models import EnrollmentRequest, EnrollmentRequestModel, StudentModel
from routers.students import students_db

router = APIRouter(prefix="/enrollments", tags=["Enrollment Requests"])


# Database-backed dictionary proxy for backward compatibility with existing tests
class EnrollmentDictProxy(collections.abc.MutableMapping):
    def __getitem__(self, key):
        init_db()
        with SessionLocal() as db:
            r = db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == key).first()
            if not r:
                raise KeyError(key)
            return r.to_dict()

    def __setitem__(self, key, val):
        init_db()
        with SessionLocal() as db:
            r = db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == key).first()
            if not r:
                data = {k: v for k, v in val.items() if k != "request_id"}
                r = EnrollmentRequestModel(request_id=key, **data)
                db.add(r)
            else:
                for k, v in val.items():
                    if hasattr(r, k):
                        setattr(r, k, v)
            db.commit()

    def __delitem__(self, key):
        init_db()
        with SessionLocal() as db:
            r = db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == key).first()
            if not r:
                raise KeyError(key)
            db.delete(r)
            db.commit()

    def __iter__(self):
        init_db()
        with SessionLocal() as db:
            return iter([r.request_id for r in db.query(EnrollmentRequestModel.request_id).all()])

    def __len__(self):
        init_db()
        with SessionLocal() as db:
            return db.query(EnrollmentRequestModel).count()

    def __contains__(self, key):
        init_db()
        with SessionLocal() as db:
            return db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == key).first() is not None

    def clear(self):
        init_db()
        with SessionLocal() as db:
            db.query(EnrollmentRequestModel).delete()
            db.commit()

    def values(self):
        init_db()
        with SessionLocal() as db:
            return [r.to_dict() for r in db.query(EnrollmentRequestModel).all()]

    def pop(self, key, default=None):
        init_db()
        with SessionLocal() as db:
            r = db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == key).first()
            if not r:
                if default is not None:
                    return default
                raise KeyError(key)
            d = r.to_dict()
            db.delete(r)
            db.commit()
            return d


enrollments_db = EnrollmentDictProxy()


@router.post("", response_model=dict)
@router.post("/", response_model=dict)
def submit_enrollment_request(req: EnrollmentRequest, db: Session = Depends(get_db)):
    """
    Submit a new student enrollment or admission request in the persistent database.
    Validates duplicate request_id (400), target student existence (404),
    and student availability/eligibility (400).
    """
    if db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == req.request_id).first():
        raise HTTPException(status_code=400, detail="Request ID exists")

    target_student = db.query(StudentModel).filter(StudentModel.student_id == req.student_id).first()
    if not target_student:
        raise HTTPException(status_code=404, detail="Student not found")

    if target_student.status in ["graduated", "inactive"]:
        raise HTTPException(status_code=400, detail="Student not available")

    new_req = EnrollmentRequestModel(
        request_id=req.request_id,
        student_id=req.student_id,
        applicant_name=req.applicant_name,
        applicant_email=req.applicant_email,
        message=req.message,
        status=req.status or "pending"
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return {"message": "Request submitted", "data": new_req.to_dict()}


@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict])
def get_requests(db: Session = Depends(get_db)):
    """
    Retrieve all enrollment requests from persistent database.
    """
    requests = db.query(EnrollmentRequestModel).all()
    return [r.to_dict() for r in requests]


@router.get("/{request_id}")
def get_request(request_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific enrollment request by ID.
    Returns 404 if not found.
    """
    req = db.query(EnrollmentRequestModel).filter(EnrollmentRequestModel.request_id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req.to_dict()
