# Task Assignment & Instructions: Pratham (S6_Pratham)

## Role & Deliverable
* **Assigned Member:** Pratham
* **Team Role:** S6 - Version Control & Git Governance Engineer
* **Core Task:** Repository Hygiene & Branch Protection
* **Assigned Files:** .gitignore

---

## Task Overview
Responsible for repository cleanliness, excluding cache/database/environment files, and configuring GitHub branch rules for the Student Management System.

---

## Step-by-Step Instructions
1. Ensure `.gitignore` ignores Python bytecode (`__pycache__`), virtual environments (`venv`, `.env`), SQLite databases (`*.db`, `students.db`), and IDE configs.
2. Verify that no binary or database runtime files are tracked by Git.
3. Configure GitHub repository branch protection rules on `main`: require Pull Request reviews before merging and require passing status checks.
4. Commit your `.gitignore` to your assigned branch (`feature/s6-git-hygiene`) and open a Pull Request.

---

## Definition of Done (DoD)
- [ ] All assigned files are implemented and clean.
- [ ] Zero syntax errors or missing dependencies.
- [ ] Automated tests pass with 0 failures (`pytest test_main.py`).
- [ ] No emojis present in code or UI files.
- [ ] Changes are committed to Git with clear commit messages.
