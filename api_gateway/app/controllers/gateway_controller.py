from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.constants import SERVICE_REGISTRY
from app.schemas.response import error_payload, success_payload
from app.services.health_service import check_service_health
from app.services.proxy_service import forward_request


async def root_info() -> dict:
    return success_payload(
        {
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
            "port": settings.port,
            "docsUrl": "/api-docs",
            "openApiUrl": "/api-docs.json",
            "routingPrefixes": {
                key: value["prefix"] for key, value in SERVICE_REGISTRY.items()
            },
        }
    )


async def gateway_health() -> dict:
    return success_payload(
        {
            "status": "healthy",
            "service": settings.app_name,
            "port": settings.port,
        }
    )


async def list_registered_routes() -> dict:
    routes = [
        {
            "serviceKey": key,
            "displayName": value["display_name"],
            "gatewayPrefix": value["prefix"],
            "upstreamBaseUrl": value["base_url"],
        }
        for key, value in SERVICE_REGISTRY.items()
    ]
    return success_payload(routes)


async def downstream_health() -> dict:
    checks = []
    for key, cfg in SERVICE_REGISTRY.items():
        checks.append(await check_service_health(key, cfg))
    return success_payload(checks)


async def proxy_to_service(request: Request, service_key: str, path: str = ""):
    service = SERVICE_REGISTRY.get(service_key)
    if not service:
        return JSONResponse(
            status_code=404,
            content=error_payload(
                f"Unknown service key: {service_key}",
                "UNKNOWN_SERVICE",
                404,
            ),
        )
    return await forward_request(request, service["base_url"], path)
