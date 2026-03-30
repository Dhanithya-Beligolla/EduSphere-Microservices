"""
Tests for health and readiness endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Health endpoint should always return 200."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "learning-materials-service"


@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient):
    """Readiness endpoint should return 200 when DB is available."""
    response = await client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
