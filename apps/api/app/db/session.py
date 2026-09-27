import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger("db")

SQLITE_PATH = Path(__file__).resolve().parents[2] / "sankalp.db"
DEFAULT_SQLITE_URL = f"sqlite:///{SQLITE_PATH}"

db_url = settings.database_url
is_sqlite = db_url.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        pool_pre_ping=not is_sqlite,
    )
    if not is_sqlite:
        with engine.connect() as conn:
            pass
except Exception as err:
    logger.warning(
        f"Database connection to '{db_url}' failed ({err}). "
        f"Falling back to SQLite database at '{DEFAULT_SQLITE_URL}'."
    )
    db_url = DEFAULT_SQLITE_URL
    is_sqlite = True
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
