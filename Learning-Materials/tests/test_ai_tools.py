"""
Tests for AI tool endpoints with feature flag ON and OFF.
"""

import pytest
from unittest.mock import patch
from httpx import AsyncClient

from tests.conftest import TEACHER_TOKEN
from tests.factories import make_material_data


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_suggest_tags_with_flag_on(client: AsyncClient):
    """AI suggest-tags should return suggestions when feature flag is on."""
    with patch("app.api.routes.ai_tools.settings") as mock_settings:
        mock_settings.enable_agent_features = True

        # Create material first
        create_resp = await client.post(
            "/api/v1/materials",
            json=make_material_data(),
            headers=auth_header(TEACHER_TOKEN),
        )
        material_id = create_resp.json()["data"]["id"]

        resp = await client.post(
            f"/api/v1/materials/{material_id}/ai/suggest-tags",
            headers=auth_header(TEACHER_TOKEN),
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["agent"] == "MetadataAgent"
        assert "suggestedTags" in body["data"]


@pytest.mark.asyncio
async def test_suggest_tags_with_flag_off(client: AsyncClient):
    """AI endpoints should return disabled message when flag is off."""
    with patch("app.api.routes.ai_tools.settings") as mock_settings:
        mock_settings.enable_agent_features = False

        create_resp = await client.post(
            "/api/v1/materials",
            json=make_material_data(),
            headers=auth_header(TEACHER_TOKEN),
        )
        material_id = create_resp.json()["data"]["id"]

        resp = await client.post(
            f"/api/v1/materials/{material_id}/ai/suggest-tags",
            headers=auth_header(TEACHER_TOKEN),
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["enabled"] is False


@pytest.mark.asyncio
async def test_classify_resource_with_flag_on(client: AsyncClient):
    """AI classify-resource should classify based on file extension."""
    with patch("app.api.routes.ai_tools.settings") as mock_settings:
        mock_settings.enable_agent_features = True

        resp = await client.post(
            "/api/v1/materials/ai/classify-resource",
            json={
                "title": "Grade 9 Science Notes",
                "fileName": "science_notes.pdf",
            },
            headers=auth_header(TEACHER_TOKEN),
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["classifiedResourceType"] == "PDF"
        assert body["data"]["confidence"] == "high"


@pytest.mark.asyncio
async def test_classify_resource_with_flag_off(client: AsyncClient):
    """AI classify-resource should return disabled when flag is off."""
    with patch("app.api.routes.ai_tools.settings") as mock_settings:
        mock_settings.enable_agent_features = False

        resp = await client.post(
            "/api/v1/materials/ai/classify-resource",
            json={"title": "Test", "fileName": "test.pdf"},
            headers=auth_header(TEACHER_TOKEN),
        )
        assert resp.status_code == 200
        assert resp.json()["data"]["enabled"] is False
