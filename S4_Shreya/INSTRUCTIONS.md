# Task Assignment & Instructions: Shreya (S4_Shreya)

## Role & Deliverable
* **Assigned Member:** Shreya
* **Team Role:** S4 - System Orchestrator & Admin Console Engineer
* **Core Task:** Application Entrypoint & Admin Management Portal
* **Assigned Files:** main.py, routers/admin.py, static/admin.html

---

## Task Overview
Responsible for assembling the root FastAPI application, configuring CORS and static mounts, routing student management APIs, and building the Registrar Administration Console.

---

## Step-by-Step Instructions
1. Maintain `main.py` ensuring all routers (`students`, `enrollments`, `admin`) are mounted along with custom frontend routes (`/`, `/health`, `/admin-dashboard`, `/portal`).
2. Verify `routers/admin.py` exposes `/admin/dashboard` metrics and `/admin/enrollments/{request_id}/status` for approving or rejecting admission requests with automatic student status cascade to `enrolled`.
3. Test `static/admin.html` by opening `http://127.0.0.1:8000/admin-dashboard` and verifying admission requests can be approved/rejected and student records can be managed.
4. Verify all tests pass with 0 failures (`pytest test_main.py`).
5. Commit your work to your assigned branch (`feature/s4-orchestration-admin`) and open a Pull Request.

---

## Definition of Done (DoD)
- [ ] All assigned files are implemented and clean.
- [ ] Zero syntax errors or missing dependencies.
- [ ] Automated tests pass with 0 failures (`pytest test_main.py`).
- [ ] No emojis present in code or UI files.
- [ ] Changes are committed to Git with clear commit messages.
