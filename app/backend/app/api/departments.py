from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth_dependencies import get_current_user, require_roles
from app.dependencies import get_db
from app.models import Department, Employee, User, UserRole
from app.schemas import DepartmentCreate, DepartmentResponse

router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"],
)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN, UserRole.HR_MANAGER)
    ),
) -> Department:
    new_department = Department(name=department.name)
    db.add(new_department)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department with this name already exists",
        ) from None

    db.refresh(new_department)
    return new_department


@router.get("", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Department]:
    return db.query(Department).order_by(Department.name).all()


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Department:
    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def update_department(
    department_id: int,
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN, UserRole.HR_MANAGER)
    ),
) -> Department:
    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    department.name = department_data.name

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department with this name already exists",
        ) from None

    db.refresh(department)
    return department


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
) -> None:
    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    has_employees = (
        db.query(Employee)
        .filter(Employee.department_id == department_id)
        .first()
        is not None
    )

    if has_employees:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete department with employees",
        )

    db.delete(department)
    db.commit()