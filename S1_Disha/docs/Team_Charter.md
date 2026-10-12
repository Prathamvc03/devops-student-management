# Student Management System — DevOps Team Charter

## 1. Project Purpose & System Overview
The **Student Management System** is a production-grade web application and DevOps automation laboratory designed to manage student registrations, admissions, enrollment workflows, and registrar operations. The system features:
- **Persistent Data Layer**: Backed by SQLite via SQLAlchemy 2.0 ORM (`database.py`, `models.py`), ensuring reliable ACID transactions and data persistence across server restarts.
- **Frontend Architecture Separation**:
  - **Public Student Portal (`static/index.html`)**: Dedicated catalog interface for students and parents to search registered students, filter by department/year/status, inspect academic profiles, and submit course admission requests. Strictly sanitized of all administrative controls.
  - **Administrative Operations Console (`static/admin.html`)**: Secure, isolated registrar operations console providing real-time KPI metrics, application review queues (approving/rejecting with automatic student status cascade to `enrolled`), and student registry management (create, delete, toggle status).
- **Automated Verification**: End-to-end Pytest suite verifying healthchecks, CRUD operations, cascade mechanics, error handling, and lifecycle transitions.
- **DevOps CI/CD & Cloud Orchestration**: Fully automated delivery pipeline using Git, Docker, Jenkins, and Kubernetes.

---

## 2. Team Member Roles & File Assignments (10 Members)

| Role ID | Member Name | Role Title | Key Responsibilities | Assigned File(s) | Technologies |
|---|---|---|---|---|---|
| **S1** | Disha | Product Owner / Team Lead | Project architecture, charter, team coordination, system specifications | `docs/Team_Charter.md`<br>`docs/Project_Architecture.md`<br>`docs/Design_System.md` | Markdown, Mermaid |
| **S2** | Sanjana | Developer 1 (Data Layer & Students) | SQLAlchemy engine, session management, ORM models, student registry & query router | `database.py`<br>`models.py`<br>`routers/__init__.py`<br>`routers/students.py` | Python, FastAPI, SQLAlchemy 2.0 |
| **S3** | Ketakee | Developer 2 (Admissions & Public UI) | Student enrollment workflow router, public student web portal | `routers/enrollments.py`<br>`static/index.html` | Python, FastAPI, HTML5, CSS3, JavaScript |
| **S4** | Shreya | Developer 3 (Admin API & Admin UI) | Application entrypoint, admin router, dedicated registrar operations console | `main.py`<br>`routers/admin.py`<br>`static/admin.html` | Python, FastAPI, HTML5, CSS3, JavaScript |
| **S5** | Shravani | QA Engineer | Dependency management, automated test suite with isolated SQLite fixtures | `requirements.txt`<br>`test_main.py` | Pytest, HTTPX, Python |
| **S6** | Pratham | Git Engineer | Version control hygiene, repository ignore rules (excluding runtime DBs) | `.gitignore` | Git, GitHub |
| **S7** | Siya | Jenkins Engineer | Multi-stage CI/CD pipeline automation (build, test, containerize, deploy) | `Jenkinsfile` | Jenkins, Declarative Pipeline |
| **S8** | Sneha | Docker Engineer | Container image packaging, build optimization, container ignore rules | `Dockerfile`<br>`.dockerignore` | Docker, Alpine/Debian Linux |
| **S9** | Yashraj | Kubernetes Engineer | Production deployment manifests, replica management, LoadBalancer networking | `k8s/deployment.yaml`<br>`k8s/service.yaml` | Kubernetes, YAML |
| **S10** | Sarang | DevOps/SRE Coordinator | Production system documentation, operational guides, API catalogs, deployment runbooks | `README.md` | Markdown |

---

## 3. Architecture & Separation Guidelines
1. **Database Persistence**:
   - `database.py` defines the SQLite engine with `check_same_thread=False` and `SessionLocal`.
   - All router endpoints access the database via FastAPI `Depends(get_db)`.
   - Runtime databases (`*.db`, `*.sqlite`, `*.sqlite3`, `students.db`) are strictly excluded from source control and container images via `.gitignore` and `.dockerignore`.
2. **Frontend UI Separation**:
   - `static/index.html` must remain strictly client-facing. No administrative API calls (`/admin/*`), status mutations, or management controls are permitted.
   - `static/admin.html` serves as the centralized registrar dashboard, interacting with `/admin/dashboard`, `/admin/enrollments/{id}`, and student management endpoints.
3. **Distribution Integrity**:
   - Each team member folder in the workspace contains only that member's designated files.
   - Zero file overlap, zero omissions, and zero runtime artifact leakage (`__pycache__`, `.pytest_cache`, `.db`).
