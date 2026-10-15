from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(StrEnum):
    ADMIN = "admin"
    HR_MANAGER = "hr_manager"
    EMPLOYEE = "employee"


class EmployeeStatus(StrEnum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    INACTIVE = "inactive"


class LeaveRequestStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department"
    )


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
    )

    position: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[EmployeeStatus] = mapped_column(
        SAEnum(
            EmployeeStatus,
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
            name="employeestatus",
        ),
        default=EmployeeStatus.ACTIVE,
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False,
    )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now(UTC),
        onupdate= datetime.now(UTC),
        nullable=False,
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees"
    )

    manager: Mapped["Employee | None"] = relationship(
        remote_side=[id],
    )

    leave_requests: Mapped[list["LeaveRequest"]] = relationship(
        back_populates="employee"
    )


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(500),
    )

    status: Mapped[LeaveRequestStatus] = mapped_column(
        SAEnum(
            LeaveRequestStatus,
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
            name="leaverequeststatus",
        ),
        default=LeaveRequestStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now(UTC),
        onupdate= datetime.now(UTC),
        nullable=False,
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="leave_requests"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SAEnum(
            UserRole,
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
            name="userrole",
        ),
        default=UserRole.EMPLOYEE,
        nullable=False,
    )

    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id"),
        unique=True,
    )

    employee: Mapped["Employee | None"] = relationship()

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user"
    )


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    is_read: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now(UTC),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="notifications"
    )


class Payroll(Base):
    __tablename__ = "payrolls"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
    )

    month: Mapped[int] = mapped_column(
        nullable=False,
    )

    year: Mapped[int] = mapped_column(
        nullable=False,
    )

    salary: Mapped[float] = mapped_column(
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now(UTC),
        onupdate= datetime.now(UTC),
        nullable=False,
    )

    employee: Mapped["Employee"] = relationship()