"""
group_main.py
FastAPI application entry point for the Group Activities Microservice.

This service owns:
  - Group creation and member management
  - Group activity lifecycle (create → assign → publish)
  - Group submissions
  - Peer evaluations
  - Results and class-level analytics

Port: 8003
Swagger UI: http://localhost:8003/docs
Redoc:      http://localhost:8003/redoc

Via API Gateway:
  http://localhost:8000/group-activities/api/v1/...
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from group_core.config import get_settings
from group_data.database import connect_to_mongo, close_mongo_connection

# Routers — one per feature
from group_routers.groups_router import router as groups_router
from group_routers.activities_router import router as activities_router
from group_routers.submissions_router import router as submissions_router
from group_routers.peer_eval_router import router as peer_eval_router
from group_routers.results_router import router as results_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


# ── Lifespan (startup / shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.SERVICE_NAME} ...")
    await connect_to_mongo(settings.MONGODB_URL, settings.DB_NAME)
    yield
    logger.info(f"Shutting down {settings.SERVICE_NAME} ...")
    await close_mongo_connection()


# ── App factory ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Group Activities Service",
    description=(
        "Microservice 03 — Group Activities & Collaboration\n\n"
        "Manages the full lifecycle of group-based learning:\n"
        "group creation, activity assignment, submissions, peer evaluation, and results.\n\n"
        "Part of the School LMS microservices architecture."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/group-activities",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include feature routers ───────────────────────────────────────────────────
app.include_router(groups_router)        # Feature 1: Group Management
app.include_router(activities_router)    # Feature 2: Activity Management
app.include_router(submissions_router)   # Feature 3: Submissions
app.include_router(peer_eval_router)     # Feature 4: Peer Evaluation
app.include_router(results_router)       # Feature 5: Results & Analytics


# ── Health check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "service": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
            "environment": settings.ENVIRONMENT,
        }
    )


# ── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "Group Activities Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "Feature 1 - Groups":       "/api/v1/groups",
            "Feature 2 - Activities":   "/api/v1/group-activities",
            "Feature 3 - Submissions":  "/api/v1/group-submissions",
            "Feature 4 - Peer Eval":    "/api/v1/peer-evaluations",
            "Feature 5 - Results":      "/api/v1/group-results/{activityId}/grade",
            "Feature 5 - Analytics":    "/api/v1/classes/{classId}/group-performance",
        },
    }
