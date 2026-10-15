
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth_dependencies import get_current_user
from app.dependencies import get_db
from app.models import (
    Employee,
    LeaveRequest,
    LeaveRequestStatus,
    User,
    UserRole,
)
from app.schemas import (
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveRequestUpdate,
)

router = APIRouter(
    prefix="/api/leave-requests",
    tags=["Leave Requests"],
)


def ensure_hr_access(current_user: User) -> None:
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.HR_MANAGER,
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


def get_leave_request_or_404(
    db: Session,
    leave_request_id: int,
) -> LeaveRequest:
    leave_request = db.get(LeaveRequest, leave_request_id)

    if leave_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found",
        )

    return leave_request


def ensure_own_request(
    leave_request: LeaveRequest,
    current_user: User,
) -> None:
    if current_user.employee_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not linked to an employee",
        )

    if leave_request.employee_id != current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found",
        )


def ensure_pending_request(leave_request: LeaveRequest) -> None:
    if leave_request.status != LeaveRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending leave requests can be modified",
        )


def validate_leave_dates(
    start_date,
    end_date,
) -> None:
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before or equal to end date",
        )


@router.get(
    "",
    response_model=list[LeaveRequestResponse],
)
def get_leave_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[LeaveRequest]:
    query = db.query(LeaveRequest)

    if current_user.role == UserRole.EMPLOYEE:
        if current_user.employee_id is None:
            return []

        query = query.filter(
            LeaveRequest.employee_id == current_user.employee_id
        )
    else:
        ensure_hr_access(current_user)

    return query.order_by(
        LeaveRequest.created_at.desc()
    ).all()


@router.get(
    "/{leave_request_id}",
    response_model=LeaveRequestResponse,
)
def get_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LeaveRequest:
    leave_request = get_leave_request_or_404(
        db,
        leave_request_id,
    )

    if current_user.role == UserRole.EMPLOYEE:
        ensure_own_request(leave_request, current_user)
    else:
        ensure_hr_access(current_user)

    return leave_request


@router.post(
    "",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_request(
    request: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LeaveRequest:
    if current_user.role == UserRole.EMPLOYEE:
        if current_user.employee_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not linked to an employee",
            )

        if request.employee_id != current_user.employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create leave requests for yourself",
            )
    else:
        ensure_hr_access(current_user)

    employee = db.get(Employee, request.employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    validate_leave_dates(
        request.start_date,
        request.end_date,
    )

    leave_request = LeaveRequest(
        employee_id=request.employee_id,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        status=LeaveRequestStatus.PENDING,
    )

    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    return leave_request


@router.patch(
    "/{leave_request_id}",
    response_model=LeaveRequestResponse,
)
def update_leave_request(
    leave_request_id: int,
    request: LeaveRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LeaveRequest:
    leave_request = get_leave_request_or_404(
        db,
        leave_request_id,
    )

    if current_user.role == UserRole.EMPLOYEE:
        ensure_own_request(leave_request, current_user)
        ensure_pending_request(leave_request)

        if request.status is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Employees cannot change leave request status",
            )
    else:
        ensure_hr_access(current_user)

    new_start_date = (
        request.start_date
        if request.start_date is not None
        else leave_request.start_date
    )
    new_end_date = (
        request.end_date
        if request.end_date is not None
        else leave_request.end_date
    )

    validate_leave_dates(new_start_date, new_end_date)

    if request.start_date is not None:
        leave_request.start_date = request.start_date

    if request.end_date is not None:
        leave_request.end_date = request.end_date

    if request.reason is not None:
        leave_request.reason = request.reason

    if request.status is not None:
        leave_request.status = request.status

    try:
        db.commit()
        db.refresh(leave_request)
    except Exception:
        db.rollback()
        raise

    return leave_request


@router.delete(
    "/{leave_request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    leave_request = get_leave_request_or_404(
        db,
        leave_request_id,
    )

    if current_user.role == UserRole.EMPLOYEE:
        ensure_own_request(leave_request, current_user)
        ensure_pending_request(leave_request)
    elif current_user.role == UserRole.ADMIN:
        pass
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can cancel their own pending requests "
            "and administrators can delete leave requests",
        )

    db.delete(leave_request)
    db.commit()
