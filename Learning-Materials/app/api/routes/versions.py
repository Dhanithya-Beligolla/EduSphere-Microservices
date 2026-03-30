"""
Version sub-resource routes.
"""

from fastapi import APIRouter, Depends, Request

from app.core.dependencies import require_material_read_access, require_material_write_access
from app.core.security import TokenClaims
from app.schemas.version import CreateVersionRequest
from app.services.version_service import VersionService
from app.utils.response import make_response

router = APIRouter()
_service = VersionService()


@router.post("/{material_id}/versions", status_code=201)
async def add_version(
    request: Request,
    material_id: str,
    body: CreateVersionRequest,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Add a new version to a learning material."""
    data = body.model_dump(by_alias=True)
    version = await _service.add_version(material_id, data, claims)
    return make_response(version, request.state.request_id)


@router.get("/{material_id}/versions")
async def list_versions(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_read_access),
):
    """List all versions for a learning material."""
    versions = await _service.list_versions(material_id, claims)
    return make_response(versions, request.state.request_id)


@router.get("/{material_id}/versions/{version_number}")
async def get_version(
    request: Request,
    material_id: str,
    version_number: int,
    claims: TokenClaims = Depends(require_material_read_access),
):
    """Get a specific version by version number."""
    version = await _service.get_version(material_id, version_number, claims)
    return make_response(version, request.state.request_id)
