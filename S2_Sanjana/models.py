"""
Data models for Student Management System.
Defines SQLAlchemy ORM models (StudentModel, EnrollmentRequestModel)
and Pydantic schemas (Student, EnrollmentRequest, StatusUpdate, StudentUpdate).
Author: Sanjana (S2_Sanjana)
"""
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# ============================================================================
# SQLAlchemy ORM Models (Persistent Database)
# ============================================================================

class StudentModel(Base):
    __tablename__ = "students"

    student_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    course = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="active")

    enrollments = relationship(
        "EnrollmentRequestModel",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "course": self.course,
            "year": self.year,
            "description": self.description,
            "status": self.status,
        }


class EnrollmentRequestModel(Base):
    __tablename__ = "enrollment_requests"

    request_id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    applicant_name = Column(String(100), nullable=False)
    applicant_email = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")

    student = relationship("StudentModel", back_populates="enrollments")

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "student_id": self.student_id,
            "applicant_name": self.applicant_name,
            "applicant_email": self.applicant_email,
            "message": self.message,
            "status": self.status,
        }


# ============================================================================
# Pydantic Schemas (Request/Response Validation)
# ============================================================================

class Student(BaseModel):
    student_id: str
    name: str
    department: str
    course: str
    year: int
    description: str
    status: str = "active"


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    course: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None


class EnrollmentRequest(BaseModel):
    request_id: str
    student_id: str
    applicant_name: str
    applicant_email: str
    message: str
    status: str = "pending"


class StatusUpdate(BaseModel):
    status: str
