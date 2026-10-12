"""
Database Seeding Script for Student Management System.
Populates initial sample students and sample enrollment applications.
"""
from database import init_db, SessionLocal
from models import StudentModel, EnrollmentRequestModel


def seed():
    init_db()
    with SessionLocal() as db:
        if db.query(StudentModel).count() > 0:
            print("Database already contains records. Skipping seed.")
            return

        sample_students = [
            StudentModel(
                student_id="STU-101",
                name="Aarav Sharma",
                department="Computer Science",
                course="B.Tech Computer Science & Engineering",
                year=3,
                description="Specializing in Distributed Cloud Computing and AI. Dean's Honour List.",
                status="active"
            ),
            StudentModel(
                student_id="STU-102",
                name="Ananya Patil",
                department="Information Technology",
                course="B.Tech Information Technology",
                year=2,
                description="Focusing on Cybersecurity and Network Infrastructure. Lead of campus coding club.",
                status="active"
            ),
            StudentModel(
                student_id="STU-103",
                name="Rohan Kulkarni",
                department="Electronics & Telecommunication",
                course="B.Tech Electronics & Telecom",
                year=4,
                description="Embedded Systems and IoT research scholar. Completed autonomous robotics internship.",
                status="enrolled"
            ),
            StudentModel(
                student_id="STU-104",
                name="Pooja Deshmukh",
                department="Mechanical Engineering",
                course="B.Tech Mechanical Engineering",
                year=3,
                description="Computational Fluid Dynamics and Thermal Systems design enthusiast.",
                status="active"
            ),
            StudentModel(
                student_id="STU-105",
                name="Aditya Joshi",
                department="Civil Engineering",
                course="B.Tech Civil & Structural Engineering",
                year=1,
                description="Incoming freshman scholar interested in Sustainable Urban Infrastructure.",
                status="active"
            ),
            StudentModel(
                student_id="STU-106",
                name="Neha Shinde",
                department="Computer Science",
                course="M.Tech Data Science & Analytics",
                year=2,
                description="Postgraduate candidate focusing on Large Language Models and Big Data Analytics.",
                status="graduated"
            ),
        ]

        db.add_all(sample_students)
        db.commit()

        sample_requests = [
            EnrollmentRequestModel(
                request_id="REQ-7001",
                student_id="STU-101",
                applicant_name="Sunil Sharma (Guardian)",
                applicant_email="sunil.sharma@example.com",
                message="Applying for Advanced Cloud Computing elective track and lab access.",
                status="pending"
            ),
            EnrollmentRequestModel(
                request_id="REQ-7002",
                student_id="STU-102",
                applicant_name="Ananya Patil (Student)",
                applicant_email="ananya.patil@example.com",
                message="Requesting admission to Honors Network Security certification module.",
                status="approved"
            )
        ]

        db.add_all(sample_requests)
        db.commit()

        print("Successfully seeded 6 students and 2 enrollment requests into students.db.")


if __name__ == "__main__":
    seed()
