"""
Student Management Router.
Handles student registration, retrieval, filtering, and updates backed by persistent database.
Author: Sanjana (S2_Sanjana)
"""
import collections.abc
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from database import get_db, SessionLocal, init_db
from models import Student, StudentModel, StudentUpdate

router = APIRouter(prefix="/students", tags=["Student Management"])


# Database-backed dictionary proxy for backward compatibility with tests and services
class StudentDictProxy(collections.abc.MutableMapping):
    def __getitem__(self, key):
        init_db()
        with SessionLocal() as db:
            s = db.query(StudentModel).filter(StudentModel.student_id == key).first()
            if not s:
                raise KeyError(key)
            return s.to_dict()

    def __setitem__(self, key, val):
        init_db()
        with SessionLocal() as db:
            s = db.query(StudentModel).filter(StudentModel.student_id == key).first()
            if not s:
                data = {k: v for k, v in val.items() if k != "student_id"}
                s = StudentModel(student_id=key, **data)
                db.add(s)
            else:
                for k, v in val.items():
                    if hasattr(s, k):
                        setattr(s, k, v)
            db.commit()

    def __delitem__(self, key):
        init_db()
        with SessionLocal() as db:
            s = db.query(StudentModel).filter(StudentModel.student_id == key).first()
            if not s:
                raise KeyError(key)
            db.delete(s)
            db.commit()

    def __iter__(self):
        init_db()
        with SessionLocal() as db:
            return iter([s.student_id for s in db.query(StudentModel.student_id).all()])

    def __len__(self):
        init_db()
        with SessionLocal() as db:
            return db.query(StudentModel).count()

    def __contains__(self, key):
        init_db()
        with SessionLocal() as db:
            return db.query(StudentModel).filter(StudentModel.student_id == key).first() is not None

    def clear(self):
        init_db()
        with SessionLocal() as db:
            db.query(StudentModel).delete()
            db.commit()

    def values(self):
        init_db()
        with SessionLocal() as db:
            return [s.to_dict() for s in db.query(StudentModel).all()]

    def pop(self, key, default=None):
        init_db()
        with SessionLocal() as db:
            s = db.query(StudentModel).filter(StudentModel.student_id == key).first()
            if not s:
                if default is not None:
                    return default
                raise KeyError(key)
            d = s.to_dict()
            db.delete(s)
            db.commit()
            return d


students_db = StudentDictProxy()


@router.post("", response_model=dict)
@router.post("/", response_model=dict)
def register_student(student: Student, db: Session = Depends(get_db)):
    """
    Register a new student in the persistent database.
    Returns 400 if student_id already exists.
    """
    existing = db.query(StudentModel).filter(StudentModel.student_id == student.student_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already exists")

    new_student = StudentModel(
        student_id=student.student_id,
        name=student.name,
        department=student.department,
        course=student.course,
        year=student.year,
        description=student.description,
        status=student.status or "active"
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Student registered", "data": new_student.to_dict()}


@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict])
def get_students(
    department: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve all registered students from persistent database.
    Supports optional filtering by department, status, and search query.
    """
    query = db.query(StudentModel)
    if department and department.lower() != "all":
        query = query.filter(StudentModel.department.ilike(f"%{department}%"))
    if status and status.lower() != "all":
        query = query.filter(StudentModel.status.ilike(f"%{status}%"))
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (StudentModel.name.ilike(search_term)) |
            (StudentModel.student_id.ilike(search_term)) |
            (StudentModel.course.ilike(search_term))
        )
    students = query.all()
    return [s.to_dict() for s in students]


@router.get("/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific student by ID.
    Returns 404 if not found.
    """
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.to_dict()


@router.put("/{student_id}")
def update_student(student_id: str, update_data: StudentUpdate, db: Session = Depends(get_db)):
    """
    Update student details (name, department, course, year, description, status).
    Returns 404 if student not found.
    """
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        if value is not None:
            setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return {"message": "Student updated", "data": student.to_dict()}


@router.delete("/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    """
    Delete a student record by ID.
    Returns 404 if student not found.
    """
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    deleted_data = student.to_dict()
    db.delete(student)
    db.commit()
    return {"message": "Student deleted", "student_id": student_id, "student": deleted_data}
