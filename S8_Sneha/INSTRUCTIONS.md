# Task Assignment & Instructions: Sneha (S8_Sneha)

## Role & Deliverable
* **Assigned Member:** Sneha
* **Team Role:** S8 - Containerization Engineer
* **Core Task:** Docker Packaging & Image Optimization
* **Assigned Files:** Dockerfile, .dockerignore

---

## Task Overview
Responsible for containerizing the Student Management System FastAPI application into an optimized, secure Docker image.

---

## Step-by-Step Instructions
1. Maintain `Dockerfile` using lightweight `python:3.10-slim` base image.
2. Ensure `.dockerignore` prevents unnecessary files (`__pycache__`, test caches, `.git`, `students.db`) from polluting the image layer.
3. Test local container build: `docker build -t student-management-system:latest .`
4. Test local container run: `docker run -p 8000:8000 student-management-system:latest`
5. Commit Docker configs to your assigned branch (`feature/s8-docker-container`) and open a Pull Request.

---

## Definition of Done (DoD)
- [ ] All assigned files are implemented and clean.
- [ ] Zero syntax errors or missing dependencies.
- [ ] Automated tests pass with 0 failures (`pytest test_main.py`).
- [ ] No emojis present in code or UI files.
- [ ] Changes are committed to Git with clear commit messages.
