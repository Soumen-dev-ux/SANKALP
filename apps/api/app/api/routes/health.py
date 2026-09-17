from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():
    return {
        "status": "ok",
        "service": "sankalp-api",
    }


@router.get("/db")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }