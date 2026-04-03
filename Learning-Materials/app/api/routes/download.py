"""
Download URL route module.
"""

from fastapi import APIRouter, Depends, Request

from app.core.dependencies import require_material_read_access
from app.core.security import TokenClaims
from app.services.download_service import DownloadService
from app.utils.response import make_response

router = APIRouter()
_service = DownloadService()


@router.get("/{material_id}/download-url")
async def get_download_url(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_read_access),
):
    """
    Generate a download URL reference for a material.
    Returns a signed URL stub with expiration.
    """
    result = await _service.generate_download_url(material_id, claims)
    return make_response(result, request.state.request_id)
