
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth_dependencies import require_roles
from app.dependencies import get_db
from app.models import (
    Department,
    Employee,
    EmployeeStatus,
    LeaveRequest,
    LeaveRequestStatus,
    User,
    UserRole,
)
from app.schemas import DashboardResponse

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN, UserRole.HR_MANAGER)
    ),
) -> DashboardResponse:
    total_employees = (
        db.query(func.count(Employee.id)).scalar() or 0
    )

    active_employees = (
        db.query(func.count(Employee.id))
        .filter(Employee.status == EmployeeStatus.ACTIVE)
        .scalar()
        or 0
    )

    on_leave_employees = (
        db.query(func.count(Employee.id))
        .filter(Employee.status == EmployeeStatus.ON_LEAVE)
        .scalar()
        or 0
    )

    inactive_employees = (
        db.query(func.count(Employee.id))
        .filter(Employee.status == EmployeeStatus.INACTIVE)
        .scalar()
        or 0
    )

    total_departments = (
        db.query(func.count(Department.id)).scalar() or 0
    )

    pending_leave_requests = (
        db.query(func.count(LeaveRequest.id))
        .filter(LeaveRequest.status == LeaveRequestStatus.PENDING)
        .scalar()
        or 0
    )

    return DashboardResponse(
        total_employees=total_employees,
        active_employees=active_employees,
        on_leave_employees=on_leave_employees,
        inactive_employees=inactive_employees,
        total_departments=total_departments,
        pending_leave_requests=pending_leave_requests,
    )


@router.get("/me")
def get_personal_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.EMPLOYEE)
    ),
) -> dict[str, int]:
    if current_user.employee_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not linked to an employee",
        )

    employee_id = current_user.employee_id

    pending_leave_requests = (
        db.query(func.count(LeaveRequest.id))
        .filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status == LeaveRequestStatus.PENDING,
        )
        .scalar()
        or 0
    )

    approved_leave_requests = (
        db.query(func.count(LeaveRequest.id))
        .filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status == LeaveRequestStatus.APPROVED,
        )
        .scalar()
        or 0
    )

    total_leave_requests = (
        db.query(func.count(LeaveRequest.id))
        .filter(LeaveRequest.employee_id == employee_id)
        .scalar()
        or 0
    )

    return {
        "total_leave_requests": total_leave_requests,
        "pending_leave_requests": pending_leave_requests,
        "approved_leave_requests": approved_leave_requests,
    }
