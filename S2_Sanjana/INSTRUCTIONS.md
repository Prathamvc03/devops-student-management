# Task Assignment & Instructions: Sanjana (S2_Sanjana)

## Role & Deliverable
* **Assigned Member:** Sanjana
* **Team Role:** S2 - Backend Core & Student Registry Engineer
* **Core Task:** Database Models & Student Registry API
* **Assigned Files:** database.py, models.py, routers/__init__.py, routers/students.py

---

## Task Overview
Responsible for setting up SQLite database persistence via SQLAlchemy, defining data schemas, and building CRUD operations for the student registry.

---

## Step-by-Step Instructions
1. Ensure `database.py` correctly initializes `sqlite:///./students.db` with proper connection pooling and thread safety.
2. Verify `models.py` contains both SQLAlchemy models and Pydantic schemas for `StudentModel`, `EnrollmentRequestModel`, `Student`, `StudentUpdate`, `EnrollmentRequest`, and `StatusUpdate`.
3. Verify `routers/students.py` exposes `/students` endpoints (GET all students with search & filter, GET by ID, POST student, PUT student, DELETE student).
4. Run `python -m pytest test_main.py` locally to verify that student registry tests pass with 0 failures.
5. Commit your work to your assigned branch (`feature/s2-students-registry`) and open a Pull Request.

---

## Definition of Done (DoD)
- [ ] All assigned files are implemented and clean.
- [ ] Zero syntax errors or missing dependencies.
- [ ] Automated tests pass with 0 failures (`pytest test_main.py`).
- [ ] No emojis present in code or UI files.
- [ ] Changes are committed to Git with clear commit messages.
