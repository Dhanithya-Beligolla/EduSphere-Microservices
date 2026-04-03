"""
Visibility route module.
"""

from fastapi import APIRouter, Depends, Request

from app.core.dependencies import require_material_read_access, require_material_write_access
from app.core.security import TokenClaims
from app.schemas.visibility import UpdateVisibilityRequest
from app.services.visibility_service import VisibilityService
from app.utils.response import make_response

router = APIRouter()
_service = VisibilityService()


@router.get("/{material_id}/visibility")
async def get_visibility(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_read_access),
):
    """Get the current visibility configuration for a material."""
    visibility = await _service.get_visibility(material_id, claims)
    return make_response(visibility, request.state.request_id)


@router.patch("/{material_id}/visibility")
async def update_visibility(
    request: Request,
    material_id: str,
    body: UpdateVisibilityRequest,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """Update the visibility scope of a material."""
    data = body.model_dump(exclude_none=True, by_alias=True)
    visibility = await _service.update_visibility(material_id, data, claims)
    return make_response(visibility, request.state.request_id)
