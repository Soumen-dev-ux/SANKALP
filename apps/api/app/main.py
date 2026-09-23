from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.db.seed import seed_db
import app.models  # noqa: F401
from app.api.routes.health import router as health_router
from app.api.routes.citizen_requests import router as citizen_request_router
# pyrefly: ignore [missing-import]
from app.api.routes.demographics import (
    router as demographic_router,
)
from app.api.routes.infrastructure import (
    router as infrastructure_router,
)
from app.api.routes.government_projects import (
    router as government_project_router,
)
from app.api.routes.regions import router as region_router
from app.api.routes.demand import router as demand_router
from app.api.routes.infrastructure_gap import (
    router as infrastructure_gap_router,
)
from app.api.routes.development_insights import(
    router as development_insight_router
)
from app.api.routes.cluster import router as cluster_router
from app.api.routes.insight_explainations import (
    router as insight_explanation_router,
)
from app.api.routes.human_reviews import router as human_review_router


from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                ALTER TABLE citizen_requests ADD COLUMN IF NOT EXISTS review_status VARCHAR(30) NOT NULL DEFAULT 'not_required';
                ALTER TABLE citizen_requests ADD COLUMN IF NOT EXISTS reviewer_note TEXT;
                ALTER TABLE citizen_requests ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;
                ALTER TABLE citizen_requests ADD COLUMN IF NOT EXISTS reviewed_category VARCHAR(100);
                ALTER TABLE citizen_requests ADD COLUMN IF NOT EXISTS reviewed_issue VARCHAR(255);
                ALTER TABLE citizen_requests ADD COLUMN IF NOT EXISTS reviewed_location VARCHAR(500);
                """
            )
        )
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router,
    prefix="/api/v1/health",
    tags=["Health"],
)
app.include_router(
    citizen_request_router,
    prefix="/api/v1",
)
app.include_router(
    demographic_router,
    prefix="/api/v1",
)
app.include_router(
    infrastructure_router,
    prefix="/api/v1",
)
app.include_router(
    government_project_router,
    prefix="/api/v1",
)
app.include_router(
    region_router,
    prefix="/api/v1",
)
app.include_router(
    demand_router,
    prefix="/api/v1",
)
app.include_router(
    infrastructure_gap_router,
    prefix="/api/v1"
)
app.include_router(
    development_insight_router,
    prefix="/api/v1"
)
app.include_router(
    cluster_router,
    prefix="/api/v1"
)
app.include_router(
    insight_explanation_router,
    prefix="/api/v1"
)
app.include_router(
    human_review_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to SANKALP API",
        "status": "running",
    }