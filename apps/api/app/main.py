from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.health import router as health_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
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


@app.get("/")
def root():
    return {
        "message": "Welcome to SANKALP API",
        "status": "running",
    }