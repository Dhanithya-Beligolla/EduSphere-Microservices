"""
Tests for material CRUD, lifecycle, and authorization.
"""

import pytest
from httpx import AsyncClient

from tests.conftest import TEACHER_TOKEN, ADMIN_TOKEN, STUDENT_TOKEN, PARENT_TOKEN
from tests.factories import make_material_data, make_link_material_data


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


# ── CREATE ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_material(client: AsyncClient):
    """Teacher should be able to create a material."""
    data = make_material_data()
    response = await client.post(
        "/api/v1/materials",
        json=data,
        headers=auth_header(TEACHER_TOKEN),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["title"] == data["title"]
    assert body["data"]["status"] == "DRAFT"
    assert body["data"]["schoolId"] == "school-001"
    assert body["errors"] == []


@pytest.mark.asyncio
async def test_create_material_without_auth(client: AsyncClient):
    """Creating a material without a token should fail."""
    data = make_material_data()
    response = await client.post("/api/v1/materials", json=data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_link_material(client: AsyncClient):
    """Should be able to create a LINK-type material with externalUrl."""
    data = make_link_material_data()
    response = await client.post(
        "/api/v1/materials",
        json=data,
        headers=auth_header(TEACHER_TOKEN),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["resourceType"] == "LINK"


# ── READ ──────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_material_by_id(client: AsyncClient):
    """Should retrieve a material by ID."""
    data = make_material_data()
    create_resp = await client.post(
        "/api/v1/materials",
        json=data,
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    get_resp = await client.get(
        f"/api/v1/materials/{material_id}",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["id"] == material_id


@pytest.mark.asyncio
async def test_list_materials(client: AsyncClient):
    """Should list materials with pagination."""
    # Create two materials
    for _ in range(2):
        await client.post(
            "/api/v1/materials",
            json=make_material_data(),
            headers=auth_header(TEACHER_TOKEN),
        )

    response = await client.get(
        "/api/v1/materials",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["totalCount"] >= 2


@pytest.mark.asyncio
async def test_student_cannot_see_draft_materials(client: AsyncClient):
    """Students should only see PUBLISHED materials."""
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    # Student tries to get the DRAFT material
    get_resp = await client.get(
        f"/api/v1/materials/{material_id}",
        headers=auth_header(STUDENT_TOKEN),
    )
    assert get_resp.status_code == 404


# ── UPDATE ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_material(client: AsyncClient):
    """Should partially update a material."""
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    update_resp = await client.patch(
        f"/api/v1/materials/{material_id}",
        json={"title": "Updated Title"},
        headers=auth_header(TEACHER_TOKEN),
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["title"] == "Updated Title"


# ── DELETE (soft) ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_soft_delete_material(client: AsyncClient):
    """Deleting should soft-delete, not hard-delete."""
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    del_resp = await client.delete(
        f"/api/v1/materials/{material_id}",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert del_resp.status_code == 200

    # Material should no longer be found
    get_resp = await client.get(
        f"/api/v1/materials/{material_id}",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert get_resp.status_code == 404


# ── LIFECYCLE ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_publish_material(client: AsyncClient):
    """Publishing a DRAFT material with complete metadata should succeed."""
    data = make_material_data()
    create_resp = await client.post(
        "/api/v1/materials",
        json=data,
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    pub_resp = await client.post(
        f"/api/v1/materials/{material_id}/publish",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert pub_resp.status_code == 200
    assert pub_resp.json()["data"]["status"] == "PUBLISHED"


@pytest.mark.asyncio
async def test_unpublish_material(client: AsyncClient):
    """Unpublishing should transition PUBLISHED -> DRAFT."""
    data = make_material_data()
    create_resp = await client.post(
        "/api/v1/materials",
        json=data,
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    # Publish first
    await client.post(
        f"/api/v1/materials/{material_id}/publish",
        headers=auth_header(TEACHER_TOKEN),
    )

    # Unpublish
    unpub_resp = await client.post(
        f"/api/v1/materials/{material_id}/unpublish",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert unpub_resp.status_code == 200
    assert unpub_resp.json()["data"]["status"] == "DRAFT"


@pytest.mark.asyncio
async def test_archive_material(client: AsyncClient):
    """Archiving a material should transition to ARCHIVED."""
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    arch_resp = await client.post(
        f"/api/v1/materials/{material_id}/archive",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert arch_resp.status_code == 200
    assert arch_resp.json()["data"]["status"] == "ARCHIVED"


@pytest.mark.asyncio
async def test_invalid_lifecycle_transition(client: AsyncClient):
    """Cannot publish an ARCHIVED material."""
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    # Archive it
    await client.post(
        f"/api/v1/materials/{material_id}/archive",
        headers=auth_header(TEACHER_TOKEN),
    )

    # Try to publish archived material
    pub_resp = await client.post(
        f"/api/v1/materials/{material_id}/publish",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert pub_resp.status_code == 422


# ── AUTHORIZATION ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_student_cannot_create_material(client: AsyncClient):
    """Students should not be able to create materials."""
    response = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(STUDENT_TOKEN),
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_parent_cannot_create_material(client: AsyncClient):
    """Parents should not be able to create materials."""
    response = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(PARENT_TOKEN),
    )
    assert response.status_code == 403
