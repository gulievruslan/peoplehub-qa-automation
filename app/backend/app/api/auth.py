from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth_dependencies import get_current_user
from app.dependencies import get_db
from app.models import User
from app.schemas import LoginRequest, LoginResponse, UserResponse
from app.security import create_access_token, verify_password

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if user is None or not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
        }
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user