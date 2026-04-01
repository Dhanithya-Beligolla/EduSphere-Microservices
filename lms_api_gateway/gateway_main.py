"""
gateway_main.py
---------------
API Gateway for the LMS Microservices Architecture.

Without this gateway, frontend clients must call 6 different ports
(8001–8006). The gateway exposes a SINGLE port (8000) and routes
requests by path prefix to the appropriate downstream service.

Run with:
    uvicorn gateway_main:app --reload --port 8000
"""

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

# ── Application ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="LMS — API Gateway",
    version="1.0.0",
    description=(
        "## Single-Entry-Point API Gateway\n\n"
        "The LMS platform comprises **6 micro­services**, each running on "
        "its own port:\n\n"
        "| Prefix | Service | Downstream |\n"
        "|--------|---------|------------|\n"
        "| `/academic` | Academic Management | `localhost:8001` |\n"
        "| `/assessment` | Homework & Assessment | `localhost:8002` |\n"
        "| `/groups` | Group Activities | `localhost:8003` |\n"
        "| `/materials` | Learning Materials | `localhost:8004` |\n"
        "| `/communication` | Communication & Student Support | `localhost:8005` |\n"
        "| `/monitoring` | Monitoring & Administration | `localhost:8006` |\n\n"
        "**Problem solved:** Without the gateway, clients must know and "
        "manage 6 different base URLs.  The gateway exposes a **single "
        "port 8000** and transparently proxies every request to the "
        "correct downstream service by stripping the path prefix and "
        "forwarding headers and body.\n\n"
        "### Example\n"
        "```\n"
        "GET http://localhost:8000/monitoring/api/v1/dashboards/principal\n"
        "  → proxied to → GET http://localhost:8006/api/v1/dashboards/principal\n"
        "```"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routing table ────────────────────────────────────────────────────────────

SERVICE_ROUTES: dict[str, str] = {
    "/academic":       "http://localhost:8001",
    "/assessment":     "http://localhost:8002",
    "/groups":         "http://localhost:8003",
    "/materials":      "http://localhost:8004",
    "/communication":  "http://localhost:8005",
    "/monitoring":     "http://localhost:8006",
}


# ── Generic reverse-proxy function ──────────────────────────────────────────

async def _proxy(request: Request, prefix: str, upstream: str) -> Response:
    """
    Forward *request* to the *upstream* service after stripping *prefix*
    from the path. All request headers (except Host) and the raw body
    are forwarded. The downstream response is returned as-is.
    """
    # Strip the service prefix from the path
    path = request.url.path.removeprefix(prefix)
    # Preserve query string
    query = str(request.url.query)
    target_url = f"{upstream}{path}"
    if query:
        target_url += f"?{query}"

    # Forward headers (drop 'host' so the downstream sees its own host)
    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() != "host"
    }

    # Read the raw request body
    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
            )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.ConnectError:
        return JSONResponse(
            status_code=502,
            content={
                "data": None,
                "meta": {"gateway": True},
                "errors": [
                    {
                        "message": f"Downstream service at {upstream} is unavailable",
                        "code": "SERVICE_UNAVAILABLE",
                    }
                ],
            },
        )


# ── Per-service proxy routes ─────────────────────────────────────────────────
# Each route captures all methods and all sub-paths under the prefix.

@app.api_route(
    "/academic/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Proxy → Academic Management Service (port 8001)",
    description="Forwards requests to the Academic Management Service after stripping the /academic prefix.",
    tags=["Proxy Routes"],
)
async def proxy_academic(request: Request):
    return await _proxy(request, "/academic", SERVICE_ROUTES["/academic"])


@app.api_route(
    "/assessment/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Proxy → Homework & Assessment Service (port 8002)",
    description="Forwards requests to the Homework & Assessment Service after stripping the /assessment prefix.",
    tags=["Proxy Routes"],
)
async def proxy_assessment(request: Request):
    return await _proxy(request, "/assessment", SERVICE_ROUTES["/assessment"])


@app.api_route(
    "/groups/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Proxy → Group Activities Service (port 8003)",
    description="Forwards requests to the Group Activities Service after stripping the /groups prefix.",
    tags=["Proxy Routes"],
)
async def proxy_groups(request: Request):
    return await _proxy(request, "/groups", SERVICE_ROUTES["/groups"])


@app.api_route(
    "/materials/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Proxy → Learning Materials Service (port 8004)",
    description="Forwards requests to the Learning Materials Service after stripping the /materials prefix.",
    tags=["Proxy Routes"],
)
async def proxy_materials(request: Request):
    return await _proxy(request, "/materials", SERVICE_ROUTES["/materials"])


@app.api_route(
    "/communication/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Proxy → Communication & Student Support Service (port 8005)",
    description="Forwards requests to the Communication & Student Support Service after stripping the /communication prefix.",
    tags=["Proxy Routes"],
)
async def proxy_communication(request: Request):
    return await _proxy(request, "/communication", SERVICE_ROUTES["/communication"])


@app.api_route(
    "/monitoring/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Proxy → Monitoring & Administration Service (port 8006)",
    description="Forwards requests to the Monitoring & Administration Service after stripping the /monitoring prefix.",
    tags=["Proxy Routes"],
)
async def proxy_monitoring(request: Request):
    return await _proxy(request, "/monitoring", SERVICE_ROUTES["/monitoring"])


# ── Root & health ────────────────────────────────────────────────────────────

@app.get(
    "/",
    summary="Gateway information",
    description="Returns metadata about the API Gateway including the full routing table.",
    tags=["Gateway Info"],
)
async def root():
    """Return gateway information and routing table."""
    return {
        "service": "LMS — API Gateway",
        "version": "1.0.0",
        "description": (
            "Single-entry-point reverse proxy for all 6 LMS microservices. "
            "Clients only need to know port 8000."
        ),
        "routingTable": {
            prefix: upstream for prefix, upstream in SERVICE_ROUTES.items()
        },
        "docsUrl": "/docs",
    }


@app.get(
    "/health",
    summary="Health check",
    description="Returns a simple health-check payload confirming the gateway is running.",
    tags=["Gateway Info"],
)
async def health():
    """Liveness probe."""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "port": 8000,
    }
