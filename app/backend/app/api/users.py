
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth_dependencies import require_roles
from app.dependencies import get_db
from app.models import Employee, User, UserRole
from app.schemas import UserResponse

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


class EmployeeLinkRequest(BaseModel):
    employee_id: int | None


@router.patch(
    "/{user_id}/employee",
    response_model=UserResponse,
)
def link_employee(
    user_id: int,
    request: EmployeeLinkRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
) -> User:
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.role != UserRole.EMPLOYEE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only employee accounts can be linked",
        )

    employee = None

    if request.employee_id is not None:
        employee = db.get(Employee, request.employee_id)

        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )

        existing_link = (
            db.query(User)
            .filter(
                User.employee_id == request.employee_id,
                User.id != user_id,
            )
            .first()
        )

        if existing_link is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee is already linked to another user",
            )

    user.employee_id = request.employee_id

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee is already linked to another user",
        ) from None

    db.refresh(user)
    return user
