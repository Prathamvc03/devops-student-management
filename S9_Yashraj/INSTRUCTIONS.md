# Task Assignment & Instructions: Yashraj (S9_Yashraj)

## Role & Deliverable
* **Assigned Member:** Yashraj
* **Team Role:** S9 - Cloud & Kubernetes Orchestration Engineer
* **Core Task:** Kubernetes Deployment & Service Manifests
* **Assigned Files:** k8s/deployment.yaml, k8s/service.yaml

---

## Task Overview
Responsible for writing Kubernetes declarative manifests for high availability, self-healing, and zero-downtime container orchestration for the Student Management System.

---

## Step-by-Step Instructions
1. Maintain `k8s/deployment.yaml` with a ReplicaSet of at least 2 pods (`student-api`), liveness/readiness probes (`/health`), and resource requests/limits.
2. Maintain `k8s/service.yaml` exposing the application via LoadBalancer / NodePort on port 80 routing to target port 8000.
3. Validate manifests with dry-run: `kubectl apply --dry-run=client -f k8s/`
4. Commit Kubernetes files to your assigned branch (`feature/s9-kubernetes-manifests`) and open a Pull Request.

---

## Definition of Done (DoD)
- [ ] All assigned files are implemented and clean.
- [ ] Zero syntax errors or missing dependencies.
- [ ] Automated tests pass with 0 failures (`pytest test_main.py`).
- [ ] No emojis present in code or UI files.
- [ ] Changes are committed to Git with clear commit messages.
