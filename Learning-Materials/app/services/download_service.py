"""
Download Service — generates download URL references.
This is a stub/placeholder. Actual signed URL generation
would connect to a file service or object storage.
"""

from datetime import datetime, timedelta
from typing import Any
import uuid

from app.core.exceptions import NotFoundError
from app.core.security import TokenClaims
from app.core.logging import get_logger
from app.repositories.material_repository import MaterialRepository

logger = get_logger("services.download")


class DownloadService:
    """Generates download URL references for learning materials."""

    def __init__(self, repo: MaterialRepository | None = None):
        self._repo = repo or MaterialRepository()

    async def generate_download_url(
        self, material_id: str, claims: TokenClaims
    ) -> dict[str, Any]:
        """
        Generate a signed download URL for a material.
        Returns a stub URL with an expiration timestamp.

        In production, this would call an upstream file service
        to generate a real signed URL.
        """
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        file_id = material.get("fileId")
        external_url = material.get("externalUrl")

        if external_url:
            # For link resources, return the external URL directly
            return {
                "materialId": material_id,
                "version": material.get("currentVersion", 1),
                "downloadUrl": external_url,
                "expiresAt": None,
                "type": "external",
            }

        # Generate a stub signed URL
        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=1)

        download_url = (
            f"https://files.example.com/download/{file_id or material_id}"
            f"?token={token}"
        )

        logger.info(
            "download_url_generated",
            material_id=material_id,
            user=claims.sub,
        )

        return {
            "materialId": material_id,
            "version": material.get("currentVersion", 1),
            "downloadUrl": download_url,
            "expiresAt": expires_at.isoformat() + "Z",
            "type": "signed",
        }
