"""
Materials CRUD and lifecycle route module.
Declares endpoints, validates input, calls services, returns envelopes.
Contains NO business logic.
"""

from fastapi import APIRouter, Depends, Request, Query

from app.core.dependencies import (
    require_authenticated_user,
    require_material_read_access,
    require_material_write_access,
)
from app.core.security import TokenClaims
from app.schemas.material import CreateMaterialRequest, UpdateMaterialRequest
from app.services.material_service import MaterialService
from app.utils.response import make_response

router = APIRouter()

# ── Service instance (stateless, safe to share) ──
_service = MaterialService()


@router.post("", status_code=201)
async def create_material(
    request: Request,
    body: CreateMaterialRequest,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Create a new learning material (starts as DRAFT)."""
    data = body.model_dump(by_alias=True)
    material = await _service.create_material(data, claims)
    return make_response(material, request.state.request_id)


@router.get("")
async def list_materials(
    request: Request,
    claims: TokenClaims = Depends(require_material_read_access),
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
    sortBy: str = Query(default="createdAt"),
    sortOrder: str = Query(default="desc", pattern="^(asc|desc)$"),
    gradeId: str | None = Query(default=None),
    subjectId: str | None = Query(default=None),
    termId: str | None = Query(default=None),
    unitId: str | None = Query(default=None),
    medium: str | None = Query(default=None),
    resourceType: str | None = Query(default=None),
    status: str | None = Query(default=None),
    tags: str | None = Query(default=None),
):
    """List learning materials with filters, pagination, and sorting."""
    filters = {
        "gradeId": gradeId,
        "subjectId": subjectId,
        "termId": termId,
        "unitId": unitId,
        "medium": medium,
        "resourceType": resourceType,
        "status": status,
        "tags": tags,
    }
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}

    result = await _service.list_materials(
        claims=claims,
        filters=filters,
        page=page,
        page_size=pageSize,
        sort_by=sortBy,
        sort_order=sortOrder,
    )
    return make_response(result, request.state.request_id)


@router.get("/{material_id}")
async def get_material(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_read_access),
):
    """Get a single learning material by ID."""
    material = await _service.get_material(material_id, claims)
    return make_response(material, request.state.request_id)


@router.patch("/{material_id}")
async def update_material(
    request: Request,
    material_id: str,
    body: UpdateMaterialRequest,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Partially update a learning material."""
    update_data = body.model_dump(exclude_none=True, by_alias=True)
    material = await _service.update_material(material_id, update_data, claims)
    return make_response(material, request.state.request_id)


@router.delete("/{material_id}")
async def delete_material(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Soft-delete (archive) a learning material."""
    await _service.soft_delete_material(material_id, claims)
    return make_response({"deleted": True}, request.state.request_id)


# ── Lifecycle endpoints ──

@router.post("/{material_id}/publish")
async def publish_material(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Publish a material (DRAFT -> PUBLISHED)."""
    material = await _service.publish_material(material_id, claims)
    return make_response(material, request.state.request_id)


@router.post("/{material_id}/unpublish")
async def unpublish_material(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Unpublish a material (PUBLISHED -> DRAFT)."""
    material = await _service.unpublish_material(material_id, claims)
    return make_response(material, request.state.request_id)


@router.post("/{material_id}/archive")
async def archive_material(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Archive a material (DRAFT|PUBLISHED -> ARCHIVED)."""
    material = await _service.archive_material(material_id, claims)
    return make_response(material, request.state.request_id)
