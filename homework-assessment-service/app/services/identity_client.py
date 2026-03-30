import httpx
from fastapi import HTTPException, status
from app.core.config import settings


async def verify_user_token(authorization: str):
    url = f"{settings.identity_service_base_url}{settings.identity_verify_endpoint}"
    headers = {"Authorization": authorization}

    try:
        async with httpx.AsyncClient(timeout=settings.identity_timeout_seconds) as client:
            response = await client.get(url, headers=headers)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Identity service unavailable",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
        )

    payload = response.json()
    if not payload.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return payload["data"]["user"]