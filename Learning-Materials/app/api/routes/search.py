"""
Search route module — full-text search with filters.
"""

from fastapi import APIRouter, Depends, Request, Query

from app.core.dependencies import require_material_read_access
from app.core.security import TokenClaims
from app.services.material_service import MaterialService
from app.utils.response import make_response

router = APIRouter()
_service = MaterialService()


@router.get("/search")
async def search_materials(
    request: Request,
    claims: TokenClaims = Depends(require_material_read_access),
    q: str = Query(default="", description="Free-text search query"),
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
):
    """Search learning materials with free-text query and filters."""
    filters = {
        "gradeId": gradeId,
        "subjectId": subjectId,
        "termId": termId,
        "unitId": unitId,
        "medium": medium,
        "resourceType": resourceType,
        "status": status,
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    result = await _service.search_materials(
        claims=claims,
        search_query=q,
        filters=filters,
        page=page,
        page_size=pageSize,
        sort_by=sortBy,
        sort_order=sortOrder,
    )
    return make_response(result, request.state.request_id)
