from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth_dependencies import get_current_user
from app.dependencies import get_db
from app.models import Employee, Payroll, User, UserRole
from app.schemas import (
    PayrollCreate,
    PayrollListResponse,
    PayrollResponse,
    PayrollSummaryResponse,
    PayrollUpdate,
)

router = APIRouter(
    prefix="/api/payroll",
    tags=["Payroll"],
)

HR_ROLES = {UserRole.HR_MANAGER}
PAYROLL_READ_ROLES = {UserRole.HR_MANAGER, UserRole.ADMIN}


def require_hr_access(current_user: User) -> None:
    """Allow access to payroll modifications for HR managers only."""
    if current_user.role not in HR_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )


def require_payroll_read_access(current_user: User) -> None:
    """Allow payroll data access for HR managers and admins."""
    if current_user.role not in PAYROLL_READ_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )


def require_employee_link(current_user: User) -> int:
    """Return the employee ID linked to the current user."""
    if current_user.employee_id is None:
        raise HTTPException(
            status_code=403,
            detail="User is not linked to an employee profile",
        )

    return current_user.employee_id


@router.get("", response_model=PayrollListResponse)
def get_payrolls(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PayrollListResponse:
    query = db.query(Payroll)

    if current_user.role == UserRole.EMPLOYEE:
        employee_id = require_employee_link(current_user)
        query = query.filter(Payroll.employee_id == employee_id)
    else:
        require_payroll_read_access(current_user)

    payrolls = query.order_by(
        Payroll.year.desc(),
        Payroll.month.desc(),
    ).all()

    total_paid = sum(
        payroll.salary
        for payroll in payrolls
        if payroll.status == "paid"
    )

    return PayrollListResponse(
        total=len(payrolls),
        total_paid=float(total_paid),
        items=[
            PayrollResponse.model_validate(payroll)
            for payroll in payrolls
        ],
    )


@router.get("/by-employee")
def get_payroll_by_employee(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_payroll_read_access(current_user)

    latest_payroll = (
        db.query(Payroll)
        .order_by(
            Payroll.year.desc(),
            Payroll.month.desc(),
        )
        .first()
    )

    if latest_payroll is None:
        return []

    payrolls = (
        db.query(
            Employee.id.label("employee_id"),
            Employee.first_name,
            Employee.last_name,
            Payroll.salary,
        )
        .join(Payroll, Payroll.employee_id == Employee.id)
        .filter(
            Payroll.month == latest_payroll.month,
            Payroll.year == latest_payroll.year,
            Payroll.status == "paid",
        )
        .order_by(Payroll.salary.desc())
        .all()
    )

    return [
        {
            "employee_id": payroll.employee_id,
            "employee_name": (
                f"{payroll.first_name} {payroll.last_name}"
            ),
            "salary": float(payroll.salary),
        }
        for payroll in payrolls
    ]


@router.get(
    "/history",
    response_model=list[PayrollSummaryResponse],
)
def get_payroll_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PayrollSummaryResponse]:
    require_payroll_read_access(current_user)

    payrolls = (
        db.query(
            Payroll.month,
            Payroll.year,
            func.sum(Payroll.salary).label("total_payroll"),
            func.count(Payroll.id).label("employees_paid"),
        )
        .filter(Payroll.status == "paid")
        .group_by(Payroll.year, Payroll.month)
        .order_by(Payroll.year.asc(), Payroll.month.asc())
        .all()
    )

    total_employees = (
        db.query(func.count(Employee.id)).scalar() or 0
    )

    return [
        PayrollSummaryResponse(
            month=payroll.month,
            year=payroll.year,
            total_payroll=float(payroll.total_payroll or 0),
            employees_paid=int(payroll.employees_paid or 0),
            total_employees=total_employees,
            average_salary=(
                float(payroll.total_payroll or 0)
                / int(payroll.employees_paid)
                if payroll.employees_paid
                else 0
            ),
            completion_percentage=(
                int(payroll.employees_paid) / total_employees * 100
                if total_employees
                else 0
            ),
        )
        for payroll in payrolls
    ]


@router.get(
    "/summary",
    response_model=PayrollSummaryResponse,
)
def get_payroll_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PayrollSummaryResponse:
    require_payroll_read_access(current_user)

    latest_payroll = (
        db.query(Payroll)
        .order_by(
            Payroll.year.desc(),
            Payroll.month.desc(),
        )
        .first()
    )

    if latest_payroll is None:
        raise HTTPException(
            status_code=404,
            detail="No payroll records found",
        )

    month = latest_payroll.month
    year = latest_payroll.year

    total_employees = (
        db.query(func.count(Employee.id)).scalar() or 0
    )

    paid_payrolls = (
        db.query(Payroll)
        .filter(
            Payroll.month == month,
            Payroll.year == year,
            Payroll.status == "paid",
        )
        .all()
    )

    total_payroll = sum(
        payroll.salary for payroll in paid_payrolls
    )
    employees_paid = len(paid_payrolls)

    return PayrollSummaryResponse(
        month=month,
        year=year,
        total_payroll=float(total_payroll),
        employees_paid=employees_paid,
        total_employees=total_employees,
        average_salary=(
            float(total_payroll) / employees_paid
            if employees_paid
            else 0
        ),
        completion_percentage=(
            employees_paid / total_employees * 100
            if total_employees
            else 0
        ),
    )


@router.get(
    "/{payroll_id}",
    response_model=PayrollResponse,
)
def get_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Payroll:
    payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found",
        )

    if current_user.role == UserRole.EMPLOYEE:
        employee_id = require_employee_link(current_user)

        if payroll.employee_id != employee_id:
            raise HTTPException(
                status_code=404,
                detail="Payroll record not found",
            )
    else:
        require_payroll_read_access(current_user)

    return payroll


@router.post("", response_model=PayrollResponse, status_code=201)
def create_payroll(
    payroll_data: PayrollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Payroll:
    require_hr_access(current_user)

    employee = db.query(Employee).filter(
        Employee.id == payroll_data.employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    existing_payroll = db.query(Payroll).filter(
        Payroll.employee_id == payroll_data.employee_id,
        Payroll.month == payroll_data.month,
        Payroll.year == payroll_data.year,
    ).first()

    if existing_payroll:
        raise HTTPException(
            status_code=400,
            detail=(
                "Payroll record already exists for this employee "
                "and month"
            ),
        )

    payroll = Payroll(
        employee_id=payroll_data.employee_id,
        month=payroll_data.month,
        year=payroll_data.year,
        salary=payroll_data.salary,
        status=payroll_data.status,
        paid_at=(
            datetime.now(UTC)
            if payroll_data.status == "paid"
            else None
        ),
    )

    db.add(payroll)
    db.commit()
    db.refresh(payroll)

    return payroll


@router.patch(
    "/{payroll_id}",
    response_model=PayrollResponse,
)
def update_payroll(
    payroll_id: int,
    payroll_data: PayrollUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Payroll:
    require_hr_access(current_user)

    payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found",
        )

    update_data = payroll_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(payroll, field, value)

    if payroll_data.status == "paid" and payroll.paid_at is None:
        payroll.paid_at = datetime.now(UTC)

    if payroll_data.status == "pending":
        payroll.paid_at = None

    db.commit()
    db.refresh(payroll)

    return payroll


@router.delete("/{payroll_id}", status_code=204)
def delete_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    require_hr_access(current_user)

    payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found",
        )

    db.delete(payroll)
    db.commit()