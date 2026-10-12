# Task Assignment & Instructions: Ketakee (S3_Ketakee)

## Role & Deliverable
* **Assigned Member:** Ketakee
* **Team Role:** S3 - Public Student Portal & Admissions API Engineer
* **Core Task:** Student Admissions/Enrollment API & Public Portal Frontend
* **Assigned Files:** routers/enrollments.py, static/index.html

---

## Task Overview
Responsible for the student enrollment application endpoints (`routers/enrollments.py`) and the responsive, accessible public student directory and admissions portal (`static/index.html`).

---

## Step-by-Step Instructions
1. Maintain `routers/enrollments.py` handling `POST /enrollments` (admission applications), `GET /enrollments` (all requests), and `GET /enrollments/{request_id}`.
2. Ensure `static/index.html` renders the modern EduTrack campus portal: left sidebar filters (search, department, academic year, enrollment status), dynamic student cards, profile modals, and admission application flow.
3. Test the frontend locally by opening `http://127.0.0.1:8000/` in your browser.
4. Verify all tests pass with 0 failures (`pytest test_main.py`).
5. Commit your files to your assigned branch (`feature/s3-student-portal`) and open a Pull Request.

---

## Definition of Done (DoD)
- [ ] All assigned files are implemented and clean.
- [ ] Zero syntax errors or missing dependencies.
- [ ] Automated tests pass with 0 failures (`pytest test_main.py`).
- [ ] No emojis present in code or UI files.
- [ ] Changes are committed to Git with clear commit messages.
