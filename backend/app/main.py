import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routes import admin_routes, ai_routes, auth_routes, doc_routes, report_routes
from app.schemas import HealthResponse
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    settings.report_path.mkdir(parents=True, exist_ok=True)
    settings.chroma_path.mkdir(parents=True, exist_ok=True)
    init_db()
    rag_service.initialize()
    logger.info("CompliancePilot AI backend started")
    yield
    logger.info("CompliancePilot AI backend shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered Compliance & Contract Intelligence Platform",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api")
app.include_router(doc_routes.router, prefix="/api")
app.include_router(ai_routes.router, prefix="/api")
app.include_router(report_routes.router, prefix="/api")
app.include_router(admin_routes.router, prefix="/api")


@app.get("/health", response_model=HealthResponse)
def health_check():
    db_status = "connected"
    try:
        from sqlalchemy import text

        from app.database import engine

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    chroma_status = "ready" if rag_service._initialized else "initializing"
    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.app_version,
        database=db_status,
        chroma=chroma_status,
    )


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }
