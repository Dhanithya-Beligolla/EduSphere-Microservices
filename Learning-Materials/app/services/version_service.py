"""
Version Service — business logic for material versioning.
"""

from typing import Any

from app.core.exceptions import NotFoundError, ValidationError
from app.core.security import TokenClaims
from app.core.logging import get_logger
from app.models.material_version import new_material_version
from app.repositories.material_repository import MaterialRepository
from app.repositories.version_repository import VersionRepository
from app.events.factory import get_event_publisher
from app.events import material_events

logger = get_logger("services.version")


class VersionService:
    """Business logic for material version management."""

    def __init__(
        self,
        material_repo: MaterialRepository | None = None,
        version_repo: VersionRepository | None = None,
    ):
        self._material_repo = material_repo or MaterialRepository()
        self._version_repo = version_repo or VersionRepository()
        self._publisher = get_event_publisher()

    async def add_version(
        self, material_id: str, data: dict[str, Any], claims: TokenClaims
    ) -> dict[str, Any]:
        """
        Add a new version to a material.
        Auto-increments version number and updates the parent material.
        """
        # Verify material exists
        material = await self._material_repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        # Get next version number
        latest_version = await self._version_repo.get_latest_version_number(material_id)
        next_version = latest_version + 1

        # Create version document
        version_doc = new_material_version(
            material_id=material_id,
            version_number=next_version,
            file_id=data.get("file_id") or data.get("fileId"),
            external_url=data.get("external_url") or data.get("externalUrl"),
            change_log=data.get("change_log") or data.get("changeLog", ""),
            created_by=claims.sub,
        )

        version_id = await self._version_repo.create(version_doc)

        # Update parent material's currentVersion and fileId
        update_data: dict[str, Any] = {
            "currentVersion": next_version,
            "updatedBy": claims.sub,
        }
        if version_doc.get("fileId"):
            update_data["fileId"] = version_doc["fileId"]
        if version_doc.get("externalUrl"):
            update_data["externalUrl"] = version_doc["externalUrl"]

        await self._material_repo.update(material_id, update_data)

        # Publish event
        event = material_events.material_versioned(material_id, next_version, claims.sub)
        await self._publisher.publish(event)

        version_doc["id"] = version_id
        if "_id" in version_doc:
            del version_doc["_id"]
        return version_doc

    async def list_versions(
        self, material_id: str, claims: TokenClaims
    ) -> list[dict[str, Any]]:
        """List all versions for a material."""
        material = await self._material_repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        return await self._version_repo.find_by_material_id(material_id)

    async def get_version(
        self, material_id: str, version_number: int, claims: TokenClaims
    ) -> dict[str, Any]:
        """Get a specific version by number."""
        material = await self._material_repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        version = await self._version_repo.find_by_version_number(
            material_id, version_number
        )
        if not version:
            raise NotFoundError("Version", str(version_number))

        return version
