"""
Health and readiness check endpoints.
"""

from fastapi import APIRouter, Response
from app.db.mongo import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("routes.health")


@router.get("/health", response_model=None)
async def health_check():
    """Basic health check — always returns 200 if the process is running."""
    return {"status": "healthy", "service": "learning-materials-service"}


@router.get("/ready", response_model=None)
async def readiness_check(response: Response):
    """
    Readiness check — verifies MongoDB connectivity.
    Returns 200 if ready, 503 if MongoDB is unreachable.
    """
    try:
        db = get_database()
        await db.command("ping")
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error("readiness_check_failed", error=str(e))
        response.status_code = 503
        return {"status": "not_ready", "database": "disconnected", "error": str(e)}
