from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.audit_log import AuditLog

from app.api.dependencies.rbac import require_admin
from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


@router.get("/access-check")
def admin_access_check(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    audit_log = AuditLog(
        user_id=current_user.id,
        action="ADMIN_ACCESS",
        resource_type="admin",
        resource_id="access-check",
    )
    db.add(audit_log)
    db.commit()

    return {
        "message": "Administrator access granted",
        "user_id": current_user.id,
        "role": current_user.role,
    }