"""
AI-assisted tool routes — deterministic agent endpoints.
Gated by ENABLE_AGENT_FEATURES feature flag.
"""

from fastapi import APIRouter, Depends, Request, Body
from typing import Any

from app.core.dependencies import require_material_write_access, require_authenticated_user
from app.core.security import TokenClaims
from app.core.config import settings
from app.agents.orchestrator import orchestrator
from app.services.material_service import MaterialService
from app.utils.response import make_response, make_error_response

router = APIRouter()
_material_service = MaterialService()


def _check_agent_features(request: Request) -> None:
    """Return a disabled response if agent features are turned off."""
    if not settings.enable_agent_features:
        return None  # Caller handles this
    return True


@router.post("/{material_id}/ai/suggest-tags")
async def suggest_tags(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_authenticated_user),
):
    """
    Suggest tags for a material based on its metadata.
    Uses deterministic keyword matching.
    """
    if not settings.enable_agent_features:
        return make_response(
            {"enabled": False, "message": "Agent features are disabled"},
            request.state.request_id,
        )

    material = await _material_service.get_material(material_id, claims)
    result = await orchestrator.suggest_tags(material)

    return make_response(
        {
            "materialId": material_id,
            "agent": "MetadataAgent",
            **result.data,
            "messages": result.messages,
        },
        request.state.request_id,
    )


@router.post("/{material_id}/ai/normalize-metadata")
async def normalize_metadata(
    request: Request,
    material_id: str,
    claims: TokenClaims = Depends(require_material_write_access),
):
    """
    Normalize material metadata — clean title, deduplicate tags, etc.
    """
    if not settings.enable_agent_features:
        return make_response(
            {"enabled": False, "message": "Agent features are disabled"},
            request.state.request_id,
        )

    material = await _material_service.get_material(material_id, claims)
    result = await orchestrator.normalize_metadata(material)

    return make_response(
        {
            "materialId": material_id,
            "agent": "MetadataAgent",
            **result.data,
            "messages": result.messages,
        },
        request.state.request_id,
    )


@router.post("/ai/classify-resource")
async def classify_resource(
    request: Request,
    body: dict[str, Any] = Body(...),
    claims: TokenClaims = Depends(require_authenticated_user),
):
    """
    Classify a resource's type and audience based on file name, URL, or title.
    Does not require an existing material — works with arbitrary input.
    """
    if not settings.enable_agent_features:
        return make_response(
            {"enabled": False, "message": "Agent features are disabled"},
            request.state.request_id,
        )

    result = await orchestrator.classify_resource(body)

    return make_response(
        {
            "agent": "ClassificationAgent",
            **result.data,
            "messages": result.messages,
        },
        request.state.request_id,
    )
