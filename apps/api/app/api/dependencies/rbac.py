from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.api.dependencies.auth import get_current_user
from app.models.user import User


def require_roles(*allowed_roles: str) -> Callable:

    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return dependency

def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )

    return current_user


def require_reviewer(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role not in {"admin", "reviewer"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reviewer access required",
        )

    return current_user


def require_analyst(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role not in {
        "admin",
        "reviewer",
        "analyst",
        "viewer",
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dashboard access required",
        )

    return current_user