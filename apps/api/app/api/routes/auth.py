from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.rate_limit import limiter

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(db, user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
@limiter.limit("10/minute")
def login(
    request: Request,
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    token = authenticate_user(db, login_data)
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user
