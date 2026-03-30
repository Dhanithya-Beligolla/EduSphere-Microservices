"""
FastAPI application bootstrap — the main entry point.

Registers:
- MongoDB lifespan
- Middleware
- Exception handlers
- API routers
- OpenAPI metadata
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.middleware import CorrelationIdMiddleware
from app.core.exceptions import (
    DomainError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
)
from app.db.mongo import mongo_lifespan
from app.api.router import api_router
from app.utils.response import make_error_response

# Initialize structured logging
setup_logging()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — manages MongoDB connection."""
    logger.info("starting_application", app=settings.app_name, version=settings.app_version)
    async with mongo_lifespan(app):
        yield
    logger.info("application_shutdown")


# ── FastAPI App ──────────────────────────────────────────────
app = FastAPI(
    title="Learning Materials Service",
    description=(
        "Backend microservice for managing digital learning materials "
        "in a Sri Lankan school LMS. Supports organization by grade, "
        "subject, term, medium, and visibility scope."
    ),
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── Middleware ────────────────────────────────────────────────
app.add_middleware(CorrelationIdMiddleware)

# ── Routers ──────────────────────────────────────────────────
app.include_router(api_router)


# ── Exception Handlers ───────────────────────────────────────

@app.exception_handler(AuthenticationError)
async def authentication_error_handler(request: Request, exc: AuthenticationError):
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=401,
        content=make_error_response(request_id, exc.code, exc.message),
    )


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(request: Request, exc: AuthorizationError):
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=403,
        content=make_error_response(request_id, exc.code, exc.message),
    )


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=404,
        content=make_error_response(request_id, exc.code, exc.message),
    )


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    """Catch-all for domain errors not handled by more specific handlers."""
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content=make_error_response(
            request_id,
            exc.code,
            exc.message,
            field=getattr(exc, "field", None),
        ),
    )


@app.exception_handler(PydanticValidationError)
async def pydantic_validation_handler(request: Request, exc: PydanticValidationError):
    request_id = getattr(request.state, "request_id", "unknown")
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error.get("loc", []))
        errors.append({
            "code": "VALIDATION_ERROR",
            "message": error.get("msg", "Validation error"),
            "field": field,
        })
    return JSONResponse(
        status_code=422,
        content={
            "data": None,
            "meta": {
                "requestId": request_id,
                "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
                "version": "v1",
            },
            "errors": errors,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected errors — logs full traceback."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("unhandled_exception", request_id=request_id, error=str(exc))
    return JSONResponse(
        status_code=500,
        content=make_error_response(
            request_id,
            "INTERNAL_ERROR",
            "An unexpected error occurred",
        ),
    )
