import os

from app.database import SessionLocal
from app.models import Department, Employee, Notification, Payroll, User, UserRole
from app.security import hash_password


ADMIN_EMAIL = os.getenv("PEOPLEHUB_ADMIN_EMAIL", "admin@peoplehub.com")
HR_EMAIL = os.getenv("PEOPLEHUB_HR_EMAIL", "hr@peoplehub.com")
EMPLOYEE_EMAIL = os.getenv("PEOPLEHUB_EMPLOYEE_EMAIL", "employee@peoplehub.com")

DEPARTMENT_NAME = "CI Department"
EMPLOYEE_PROFILE_EMAIL = "employee.profile@example.com"


def get_or_create_user(db, email: str, password_env: str, role: UserRole) -> User:
    user = db.query(User).filter(User.email == email).first()

    if user:
        return user

    user = User(
        email=email,
        password_hash=hash_password(os.environ[password_env]),
        role=role,
    )
    db.add(user)
    db.flush()
    return user


def get_or_create_department(db) -> Department:
    department = db.query(Department).filter(Department.name == DEPARTMENT_NAME).first()

    if department:
        return department

    department = Department(name=DEPARTMENT_NAME)
    db.add(department)
    db.flush()
    return department


def get_or_create_employee(db, department_id: int) -> Employee:
    employee = db.query(Employee).filter(Employee.email == EMPLOYEE_PROFILE_EMAIL).first()

    if employee:
        return employee

    employee = Employee(
        first_name="CI",
        last_name="Employee",
        email=EMPLOYEE_PROFILE_EMAIL,
        position="QA Engineer",
        status="active",
        department_id=department_id,
    )
    db.add(employee)
    db.flush()
    return employee


def get_employee_for_user(db, employee_user: User, department_id: int) -> Employee:
    if employee_user.employee_id is not None:
        employee = db.get(Employee, employee_user.employee_id)

        if employee is not None:
            return employee

    employee = db.query(Employee).filter(Employee.email == EMPLOYEE_PROFILE_EMAIL).first()

    if employee is None:
        employee = get_or_create_employee(db, department_id)

    employee_user.employee_id = employee.id
    db.flush()
    return employee


def seed_users(db) -> Employee:
    admin = get_or_create_user(
        db,
        ADMIN_EMAIL,
        "PEOPLEHUB_ADMIN_PASSWORD",
        UserRole.ADMIN,
    )
    hr_manager = get_or_create_user(
        db,
        HR_EMAIL,
        "PEOPLEHUB_HR_PASSWORD",
        UserRole.HR_MANAGER,
    )
    employee_user = get_or_create_user(
        db,
        EMPLOYEE_EMAIL,
        "PEOPLEHUB_EMPLOYEE_PASSWORD",
        UserRole.EMPLOYEE,
    )

    department = get_or_create_department(db)
    employee = get_employee_for_user(db, employee_user, department.id)

    print(f"Admin user ready: {admin.email}")
    print(f"HR Manager user ready: {hr_manager.email}")
    print(f"Employee user ready: {employee_user.email}")
    print(f"Employee profile ready: {employee.id}")

    return employee


def seed_notifications(db) -> None:
    admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()

    if admin is None:
        return

    existing_count = db.query(Notification).filter(Notification.user_id == admin.id).count()

    if existing_count:
        print("Notifications already exist")
        return

    db.add_all(
        [
            Notification(
                user_id=admin.id,
                title="Leave request",
                message="A new leave request was submitted.",
                is_read=False,
            ),
            Notification(
                user_id=admin.id,
                title="New employee",
                message="A new employee joined the organization.",
                is_read=False,
            ),
            Notification(
                user_id=admin.id,
                title="Profile updated",
                message="An employee profile was updated.",
                is_read=False,
            ),
        ]
    )
    db.flush()
    print("Notifications created")


def seed_payroll(db, employee: Employee) -> None:
    existing_count = db.query(Payroll).filter(Payroll.employee_id == employee.id).count()

    if existing_count:
        print("Payroll records already exist")
        return

    db.add_all(
        [
            Payroll(
                employee_id=employee.id,
                month=month,
                year=2026,
                salary=4200,
                status="paid",
            )
            for month in range(5, 10)
        ]
    )
    db.flush()
    print("Payroll records created")


def seed() -> None:
    db = SessionLocal()

    try:
        employee = seed_users(db)
        seed_notifications(db)
        seed_payroll(db, employee)
        db.commit()
        print("Seed completed successfully")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()