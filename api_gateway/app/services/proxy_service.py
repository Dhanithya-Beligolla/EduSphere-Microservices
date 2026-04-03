import httpx
from fastapi import Request
from fastapi.responses import JSONResponse, Response

from app.core.config import settings
from app.schemas.response import error_payload


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


async def forward_request(request: Request, upstream_base_url: str, upstream_path: str = "") -> Response:
    target_url = f"{upstream_base_url.rstrip('/')}/{upstream_path.lstrip('/')}"
    query = request.url.query
    if query:
        target_url = f"{target_url}?{query}"

    forward_headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in HOP_BY_HOP_HEADERS
    }

    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=settings.proxy_timeout_seconds) as client:
            upstream_response = await client.request(
                method=request.method,
                url=target_url,
                headers=forward_headers,
                content=body,
            )

        response_headers = {
            k: v
            for k, v in upstream_response.headers.items()
            if k.lower() not in HOP_BY_HOP_HEADERS
        }

        return Response(
            content=upstream_response.content,
            status_code=upstream_response.status_code,
            headers=response_headers,
        )
    except httpx.ConnectError:
        return JSONResponse(
            status_code=502,
            content=error_payload(
                f"Downstream service unavailable: {upstream_base_url}",
                "DOWNSTREAM_UNAVAILABLE",
                502,
            ),
        )
    except httpx.TimeoutException:
        return JSONResponse(
            status_code=504,
            content=error_payload(
                f"Downstream timeout: {upstream_base_url}",
                "DOWNSTREAM_TIMEOUT",
                504,
            ),
        )
