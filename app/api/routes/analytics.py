"""
Analytics stub route module.
"""

from fastapi import APIRouter, Depends, Request

from app.core.dependencies import require_material_read_access
from app.core.security import TokenClaims
from app.utils.response import make_response

router = APIRouter()


@router.get("/{material_id}/analytics")
async def get_material_analytics(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_read_access),
):
    """
    Get analytics for a material — stub endpoint.
    Returns placeholder metrics for future implementation.
    """
    analytics_data = {
        "materialId": material_id,
        "viewCount": 0,
        "downloadCount": 0,
        "uniqueViewers": 0,
        "lastAccessedAt": None,
        "note": "Analytics data is a placeholder — will be populated by the analytics service",
    }
    return make_response(analytics_data, request.state.request_id)
