# Task Assignment & Instructions: Shravani (S5_Shravani)

## Role & Deliverable
* **Assigned Member:** Shravani
* **Team Role:** S5 - QA & Test Automation Engineer
* **Core Task:** Dependency Management & Automated Pytest Suite
* **Assigned Files:** requirements.txt, test_main.py

---

## Task Overview
Responsible for managing project dependencies and authoring the automated test suite ensuring 100% endpoint coverage, zero regressions, and full lifecycle validation of the Student Management System.

---

## Step-by-Step Instructions
1. Review `requirements.txt` to ensure all core packages (`fastapi`, `uvicorn`, `pydantic`, `pytest`, `httpx`, `sqlalchemy`) are pinned.
2. Execute the test suite in terminal: `pytest test_main.py -v`.
3. Ensure all 29 unit, integration, cascade, and lifecycle tests pass with 0 failures.
4. Verify that the autouse database reset fixture guarantees test isolation without polluting persistent data.
5. Commit your test files to your assigned branch (`feature/s5-qa-tests`) and open a Pull Request.

---

## Definition of Done (DoD)
- [ ] All assigned files are implemented and clean.
- [ ] Zero syntax errors or missing dependencies.
- [ ] Automated tests pass with 0 failures (`pytest test_main.py`).
- [ ] No emojis present in code or UI files.
- [ ] Changes are committed to Git with clear commit messages.
