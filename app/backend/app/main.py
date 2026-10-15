from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.departments import router as departments_router
from app.api.employees import router as employees_router
from app.api.leave_requests import router as leave_requests_router
from app.api.notifications import router as notifications_router
from app.api.users import router as users_router
from app.api.payroll import router as payroll_router
from app.database import engine

app = FastAPI(
    title="PeopleHub API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(departments_router)
app.include_router(employees_router)
app.include_router(leave_requests_router)
app.include_router(notifications_router)
app.include_router(payroll_router)
app.include_router(users_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def database_health_check() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to PeopleHub API"}