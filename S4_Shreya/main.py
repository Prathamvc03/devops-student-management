"""
Main Application Entrypoint.
FastAPI application mounting routers, static portal, CORS, health probes,
and persistent database initialization for Student Management System.
Author: Shreya (S4_Shreya)
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import init_db
from routers import students, enrollments, admin

# Initialize persistent database tables on startup
init_db()

app = FastAPI(
    title="Student Management System",
    version="1.0.0",
    description="Persistent REST API for managing student records, admissions, and academic administration."
)

# Enable CORS for browser frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(students.router)
app.include_router(enrollments.router)
app.include_router(admin.router)

# Mount static frontend directory safely if present
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    static_dir = "static"

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/")
def root():
    """API Root Health Check returning JSON status."""
    return {
        "status": "ok",
        "message": "Student Management System API is running"
    }


@app.get("/health")
def health_check():
    """Kubernetes Liveness and Readiness probe endpoint."""
    return {"status": "ok"}


@app.get("/admin-dashboard")
def admin_dashboard_redirect():
    """Redirect shortcut to admin operations dashboard."""
    return RedirectResponse(url="/static/admin.html")


@app.get("/portal")
def portal_redirect():
    """Redirect shortcut to public student portal."""
    return RedirectResponse(url="/static/index.html")
