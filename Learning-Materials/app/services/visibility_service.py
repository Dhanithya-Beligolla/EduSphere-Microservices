"""
Visibility Service — handles visibility scope operations for materials.
"""

from typing import Any

from app.core.exceptions import NotFoundError
from app.core.security import TokenClaims
from app.core.constants import Role, VisibilityScopeType
from app.core.logging import get_logger
from app.repositories.material_repository import MaterialRepository

logger = get_logger("services.visibility")


class VisibilityService:
    """Business logic for material visibility management."""

    def __init__(self, repo: MaterialRepository | None = None):
        self._repo = repo or MaterialRepository()

    async def get_visibility(
        self, material_id: str, claims: TokenClaims
    ) -> dict[str, Any]:
        """Get the current visibility configuration for a material."""
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        return material.get("visibility", {})

    async def update_visibility(
        self, material_id: str, visibility_data: dict[str, Any], claims: TokenClaims
    ) -> dict[str, Any]:
        """Update the visibility scope of a material."""
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        current_visibility = material.get("visibility", {})

        # Merge updates into current visibility
        for key, value in visibility_data.items():
            if value is not None:
                current_visibility[key] = value

        # Ensure schoolId is always present
        current_visibility["schoolId"] = claims.school_id

        updated = await self._repo.update(material_id, {
            "visibility": current_visibility,
            "updatedBy": claims.sub,
        })

        if not updated:
            raise NotFoundError("Material", material_id)

        return updated.get("visibility", {})

    @staticmethod
    def can_user_access(material: dict[str, Any], claims: TokenClaims) -> bool:
        """
        Visibility resolution helper — determines whether a user can access
        a material based on their role and the material's visibility scope.

        Returns True if access is granted.
        """
        # Admin/Principal can see everything in their school
        if claims.is_admin_or_principal():
            return material.get("schoolId") == claims.school_id

        visibility = material.get("visibility", {})
        scope_type = visibility.get("scopeType", "SCHOOL")

        # School-wide visibility — everyone in the school can see it
        if scope_type == VisibilityScopeType.SCHOOL.value:
            return material.get("schoolId") == claims.school_id

        # Grade-level visibility
        if scope_type == VisibilityScopeType.GRADE.value:
            grade_ids = set(visibility.get("gradeIds", []))
            return bool(grade_ids)  # Simplified — needs user's grade from claims

        # Class-level visibility
        if scope_type == VisibilityScopeType.CLASS.value:
            class_ids = set(visibility.get("classIds", []))
            user_classes = set(claims.class_ids)
            return bool(class_ids & user_classes)

        # Subject-level visibility
        if scope_type == VisibilityScopeType.SUBJECT.value:
            subject_ids = set(visibility.get("subjectIds", []))
            user_subjects = set(claims.subject_ids)
            return bool(subject_ids & user_subjects)

        # Section-level visibility
        if scope_type == VisibilityScopeType.SECTION.value:
            section_ids = set(visibility.get("sectionIds", []))
            user_sections = set(claims.section_ids)
            return bool(section_ids & user_sections)

        # Stream-level visibility
        if scope_type == VisibilityScopeType.STREAM.value:
            stream_ids = set(visibility.get("streamIds", []))
            user_streams = set(claims.stream_ids)
            return bool(stream_ids & user_streams)

        return False
