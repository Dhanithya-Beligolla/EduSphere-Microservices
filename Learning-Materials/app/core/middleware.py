"""
ASGI middleware for correlation-ID propagation and request logging.
"""

import uuid
import time
import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Injects a correlation/request ID into every request.
    - Uses incoming X-Request-ID header if present.
    - Otherwise generates a UUID4.
    - Binds the ID to structlog context vars for all downstream log calls.
    - Adds X-Request-ID to the response.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Bind to structlog context so all logs within this request carry the ID
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        # Store on request state for downstream access
        request.state.request_id = request_id

        logger = structlog.get_logger("request")
        start_time = time.perf_counter()

        logger.info(
            "request_started",
            method=request.method,
            path=str(request.url.path),
            query=str(request.url.query) if request.url.query else None,
        )

        try:
            response = await call_next(request)
        except Exception:
            logger.exception("request_failed")
            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "request_completed",
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        response.headers["X-Request-ID"] = request_id
        return response
