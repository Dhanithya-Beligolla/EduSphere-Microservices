"""
monitoring_main.py
------------------
FastAPI application entry-point for the LMS Monitoring & Administration
Service (Service 06 of 6 in the LMS microservices architecture).

Run with:
    uvicorn lms_monitoring_service.monitoring_main:app --reload --port 4007
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse

# Relative imports for the three routers
from .monitoring_routers.monitoring_dashboards import router as dashboards_router
from .monitoring_routers.monitoring_reports import router as reports_router
from .monitoring_routers.monitoring_risk_audit import router as risk_audit_router
from .monitoring_core.config import settings
from .monitoring_core.database import Base, SessionLocal, engine
from .monitoring_data.monitoring_seed import seed_initial_data

# ── Application factory ─────────────────────────────────────────────────────

app = FastAPI(
    title="LMS — Monitoring & Administration Service",
    version="1.0.0",
    description=(
        "## Service 06 of 6 — LMS Microservices Architecture\n\n"
        "The **Monitoring & Administration Service** aggregates data from "
        "all five upstream micro­services:\n\n"
        "| # | Service | Port |\n"
        "|---|---------|------|\n"
        "| 01 | Academic Management | 3001 |\n"
        "| 02 | Homework & Assessment | 3002 |\n"
        "| 03 | Group Activities | 3003 |\n"
        "| 04 | Learning Materials | 3004 |\n"
        "| 05 | Communication & Student Support | 3005 |\n"
        "| **06** | **Monitoring & Administration** | **4007** |\n\n"
        "### Key capabilities\n"
        "- **Role-based dashboards** for Principal, Sectional Head, "
        "Class Teacher, and Subject Teacher — each role sees only the "
        "data relevant to their scope.\n"
        "- **Reports** — assignment completion, academic risk, and "
        "learning-material usage, with async PDF/CSV export via report "
        "jobs.\n"
        "- **Risk detection** — configurable rules that flag at-risk "
        "students based on submission rate, average score, and "
        "attendance.\n"
        "- **Audit trail** — tamper-evident log of every significant "
        "user action.\n"
        "- **KPI snapshots & intervention queue** — track school-wide "
        "metrics over time and manage follow-up actions for at-risk "
        "students.\n\n"
        "All endpoints return the standard response envelope:\n"
        "```json\n"
        '{"data": ..., "meta": {"requestId": "...", "timestamp": "...", '
        '"version": "v1"}, "errors": []}\n'
        "```\n\n"
        "This service consumes events asynchronously from upstream "
        "services and exposes read-optimised models through the API."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS middleware — allow all origins for development ──────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ────────────────────────────────────────────────────────

app.include_router(dashboards_router)
app.include_router(reports_router)
app.include_router(risk_audit_router)


@app.get("/api-docs", include_in_schema=False)
async def swagger_docs_alias():
    """Serve Swagger UI at /api-docs for consistency across services."""
    return get_swagger_ui_html(
        openapi_url="/api-docs.json",
        title="LMS Monitoring Service API Docs",
    )


@app.get("/api-docs.json", include_in_schema=False)
async def swagger_openapi_alias():
    """Serve OpenAPI JSON at /api-docs.json for tooling integration."""
    return JSONResponse(app.openapi())


# ── Root & health endpoints ─────────────────────────────────────────────────

@app.get(
    "/",
    summary="Service information",
    description="Returns metadata about the Monitoring & Administration Service.",
    tags=["Service Info"],
)
async def root():
    """Return basic service information."""
    return {
        "service": "LMS — Monitoring & Administration Service",
        "version": "1.0.0",
        "description": (
            "Service 06 of 6 in the LMS microservices architecture. "
            "Provides role-based dashboards, reports, risk detection, "
            "and audit trail for a Sri Lankan school."
        ),
        "docsUrl": "/docs",
        "redocUrl": "/redoc",
        "endpoints": {
            "dashboards": "/api/v1/dashboards",
            "reports": "/api/v1/reports",
            "reportJobs": "/api/v1/report-jobs",
            "kpis": "/api/v1/kpis",
            "interventions": "/api/v1/interventions",
            "snapshots": "/api/v1/snapshots",
            "riskRules": "/api/v1/risk-rules",
            "auditViews": "/api/v1/audit-views",
        },
    }


@app.get(
    "/health",
    summary="Health check",
    description="Returns a simple health-check payload confirming the service is running.",
    tags=["Service Info"],
)
async def health():
    """Liveness probe for container orchestrators."""
    return {
        "status": "healthy",
        "service": "monitoring-service",
        "port": settings.port,
    }


@app.on_event("startup")
def startup_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
