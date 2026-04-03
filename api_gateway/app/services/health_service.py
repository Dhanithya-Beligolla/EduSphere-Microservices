import httpx

from app.core.config import settings


async def check_service_health(service_key: str, service_config: dict) -> dict:
    health_url = f"{service_config['base_url'].rstrip('/')}{service_config['health_path']}"
    try:
        async with httpx.AsyncClient(timeout=settings.proxy_timeout_seconds) as client:
            response = await client.get(health_url)
        return {
            "serviceKey": service_key,
            "name": service_config["display_name"],
            "baseUrl": service_config["base_url"],
            "healthUrl": health_url,
            "status": "UP" if response.status_code < 500 else "DEGRADED",
            "httpStatus": response.status_code,
        }
    except Exception as exc:
        return {
            "serviceKey": service_key,
            "name": service_config["display_name"],
            "baseUrl": service_config["base_url"],
            "healthUrl": health_url,
            "status": "DOWN",
            "error": str(exc),
        }
