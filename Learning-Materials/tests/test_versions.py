"""
Tests for material version endpoints.
"""

import pytest
from httpx import AsyncClient

from tests.conftest import TEACHER_TOKEN
from tests.factories import make_material_data, make_version_data


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_add_version(client: AsyncClient):
    """Adding a version should auto-increment version number."""
    # Create material
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    # Add version
    version_data = make_version_data()
    ver_resp = await client.post(
        f"/api/v1/materials/{material_id}/versions",
        json=version_data,
        headers=auth_header(TEACHER_TOKEN),
    )
    assert ver_resp.status_code == 201
    body = ver_resp.json()
    assert body["data"]["versionNumber"] == 1


@pytest.mark.asyncio
async def test_list_versions(client: AsyncClient):
    """Should list all versions for a material."""
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    # Add two versions
    for i in range(2):
        await client.post(
            f"/api/v1/materials/{material_id}/versions",
            json=make_version_data(change_log=f"Version {i+1} update"),
            headers=auth_header(TEACHER_TOKEN),
        )

    list_resp = await client.get(
        f"/api/v1/materials/{material_id}/versions",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert list_resp.status_code == 200
    versions = list_resp.json()["data"]
    assert len(versions) == 2


@pytest.mark.asyncio
async def test_get_specific_version(client: AsyncClient):
    """Should retrieve a specific version by number."""
    create_resp = await client.post(
        "/api/v1/materials",
        json=make_material_data(),
        headers=auth_header(TEACHER_TOKEN),
    )
    material_id = create_resp.json()["data"]["id"]

    await client.post(
        f"/api/v1/materials/{material_id}/versions",
        json=make_version_data(),
        headers=auth_header(TEACHER_TOKEN),
    )

    ver_resp = await client.get(
        f"/api/v1/materials/{material_id}/versions/1",
        headers=auth_header(TEACHER_TOKEN),
    )
    assert ver_resp.status_code == 200
    assert ver_resp.json()["data"]["versionNumber"] == 1
