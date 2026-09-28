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
# pyrefly: ignore [missing-import]
from app.api.routes.auth import router as auth_router

from sqlalchemy import text
from app.api.routes.admin import router as admin_router
from app.api.routes import reviewer 
from app.api.routes.intelligence import router as intelligence_router


import logging
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("sankalp")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        if engine.dialect.name == "postgresql":
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
        else:
            # SQLite auto-migration for existing dev/test databases
            try:
                res = conn.execute(text("PRAGMA table_info(citizen_requests)")).fetchall()
                existing_cols = {row[1] for row in res}
                if existing_cols:
                    if "review_status" not in existing_cols:
                        conn.execute(text("ALTER TABLE citizen_requests ADD COLUMN review_status VARCHAR(30) NOT NULL DEFAULT 'not_required'"))
                    if "reviewer_note" not in existing_cols:
                        conn.execute(text("ALTER TABLE citizen_requests ADD COLUMN reviewer_note TEXT"))
                    if "reviewed_at" not in existing_cols:
                        conn.execute(text("ALTER TABLE citizen_requests ADD COLUMN reviewed_at TIMESTAMP"))
                    if "reviewed_category" not in existing_cols:
                        conn.execute(text("ALTER TABLE citizen_requests ADD COLUMN reviewed_category VARCHAR(100)"))
                    if "reviewed_issue" not in existing_cols:
                        conn.execute(text("ALTER TABLE citizen_requests ADD COLUMN reviewed_issue VARCHAR(255)"))
                    if "reviewed_location" not in existing_cols:
                        conn.execute(text("ALTER TABLE citizen_requests ADD COLUMN reviewed_location VARCHAR(500)"))
            except Exception as ex:
                logger.warning(f"SQLite auto-migration notice: {ex}")
    try:
        db = SessionLocal()
        try:
            seed_db(db)
        finally:
            db.close()
    except Exception as e:
        print(f"Database seed notice: {e}")
    yield




from app.core.rate_limit import limiter

try:
    # pyrefly: ignore [missing-import]
    from slowapi import _rate_limit_exceeded_handler
    # pyrefly: ignore [missing-import]
    from slowapi.errors import RateLimitExceeded
    HAS_SLOWAPI = True
except ImportError:
    HAS_SLOWAPI = False

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    lifespan=lifespan,
)
app.state.limiter = limiter
if HAS_SLOWAPI:
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



@app.middleware("http")
async def add_security_headers_and_log(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.4f}s")
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.jsdelivr.net; "
            "worker-src 'self' blob:;"
        )
    else:
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": str(exc.status_code), "message": exc.detail}}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid input format or validation failed."}}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
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
app.include_router(
    auth_router,
    prefix="/api/v1",
)
app.include_router(
    admin_router,
    prefix="/api/v1"
)
app.include_router(
    reviewer.router,
    prefix="/api/v1"
)
app.include_router(
    intelligence_router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to SANKALP API",
        "status": "running",
    }