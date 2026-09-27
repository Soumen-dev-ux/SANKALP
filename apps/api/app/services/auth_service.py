from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.auth import UserCreate, UserLogin


def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )

    user = User(
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
        full_name=user_data.full_name,
        role="reviewer",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    login_data: UserLogin,
) -> str:

    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if user is None:
        failed_log = AuditLog(
            user_id=None,
            action="FAILED_LOGIN",
            resource_type="auth",
            metadata={"email": login_data.email, "reason": "user_not_found"}
        )
        db.add(failed_log)
        db.commit()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        login_data.password,
        user.password_hash,
    ):
        failed_log = AuditLog(
            user_id=user.id,
            action="FAILED_LOGIN",
            resource_type="auth",
            metadata={"email": login_data.email, "reason": "wrong_password"}
        )
        db.add(failed_log)
        db.commit()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive",
        )

    audit_log = AuditLog(
        user_id=user.id,
        action="USER_LOGIN",
        resource_type="auth",
        resource_id=str(user.id),
    )
    db.add(audit_log)
    db.commit()

    return create_access_token(user.id)