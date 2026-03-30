"""
Material Service — core business logic for learning materials.
Implements lifecycle management, CRUD, authorization scope enforcement,
and event publishing.

This service is independent of FastAPI request objects.
"""

from datetime import datetime
from typing import Any

from app.core.constants import MaterialStatus, Role, ResourceType, ADMIN_ROLES
from app.core.exceptions import (
    NotFoundError,
    LifecycleError,
    PublishValidationError,
    AuthorizationError,
    ValidationError,
)
from app.core.security import TokenClaims
from app.core.logging import get_logger
from app.models.learning_material import new_learning_material
from app.repositories.material_repository import MaterialRepository
from app.events.factory import get_event_publisher
from app.events import material_events
from app.utils.object_id import serialize_doc
from app.utils.pagination import calc_total_pages

logger = get_logger("services.material")


class MaterialService:
    """Business logic for learning material operations."""

    def __init__(self, repo: MaterialRepository | None = None):
        self._repo = repo or MaterialRepository()
        self._publisher = get_event_publisher()

    # ── CRUD ──────────────────────────────────────────────────

    async def create_material(
        self, data: dict[str, Any], claims: TokenClaims
    ) -> dict[str, Any]:
        """
        Create a new learning material in DRAFT status.
        Enforces that teachers can only create for their assigned subjects.
        """
        # Scope enforcement: subject teachers can only create for their subjects
        if claims.has_role(Role.SUBJECT_TEACHER) and not claims.is_admin_or_principal():
            subject_id = data.get("subject_id") or data.get("subjectId")
            if subject_id and claims.subject_ids and subject_id not in claims.subject_ids:
                raise AuthorizationError(
                    f"You are not assigned to subject '{subject_id}'"
                )

        # Validate resource-type specific requirements
        resource_type = data.get("resource_type") or data.get("resourceType")
        file_id = data.get("file_id") or data.get("fileId")
        external_url = data.get("external_url") or data.get("externalUrl")

        if resource_type == ResourceType.LINK.value and not external_url:
            raise ValidationError("LINK resources require an externalUrl", field="externalUrl")

        # Build the document
        doc = new_learning_material(
            title=data["title"],
            description=data.get("description"),
            subject_id=data.get("subject_id") or data.get("subjectId"),
            grade_id=data.get("grade_id") or data.get("gradeId"),
            term_id=data.get("term_id") or data.get("termId"),
            unit_id=data.get("unit_id") or data.get("unitId"),
            medium=data.get("medium"),
            resource_type=resource_type,
            tags=data.get("tags", []),
            visibility=data.get("visibility"),
            file_id=file_id,
            external_url=external_url,
            thumbnail_url=data.get("thumbnail_url") or data.get("thumbnailUrl"),
            language=data.get("language"),
            school_id=claims.school_id,
            created_by=claims.sub,
        )

        material_id = await self._repo.create(doc)

        # Publish event
        event = material_events.material_created(material_id, claims.sub, data["title"])
        await self._publisher.publish(event)

        # Return the created material
        return await self.get_material(material_id, claims)

    async def get_material(
        self, material_id: str, claims: TokenClaims
    ) -> dict[str, Any]:
        """Get a single material by ID with authorization checks."""
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        # School scope check
        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        # Students/parents can only see PUBLISHED materials
        if claims.has_any_role({Role.STUDENT, Role.PARENT}):
            if material.get("status") != MaterialStatus.PUBLISHED.value:
                raise NotFoundError("Material", material_id)

        return material

    async def list_materials(
        self,
        claims: TokenClaims,
        filters: dict[str, Any] | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "createdAt",
        sort_order: str = "desc",
    ) -> dict[str, Any]:
        """
        List materials with filtering, pagination, and role-based visibility.
        """
        query: dict[str, Any] = {"schoolId": claims.school_id}

        # Students and parents can only see published materials
        if claims.has_any_role({Role.STUDENT, Role.PARENT}):
            query["status"] = MaterialStatus.PUBLISHED.value
        elif filters and filters.get("status"):
            query["status"] = filters["status"]

        # Apply additional filters
        if filters:
            for key in ["gradeId", "subjectId", "termId", "unitId", "medium", "resourceType"]:
                if filters.get(key):
                    query[key] = filters[key]

            # Tag filter
            if filters.get("tags"):
                tag_list = [t.strip() for t in filters["tags"].split(",") if t.strip()]
                if tag_list:
                    query["tags"] = {"$in": tag_list}

        items, total_count = await self._repo.find_many(
            filter_query=query,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return {
            "items": items,
            "totalCount": total_count,
            "page": page,
            "pageSize": page_size,
            "totalPages": calc_total_pages(total_count, page_size),
        }

    async def search_materials(
        self,
        claims: TokenClaims,
        search_query: str,
        filters: dict[str, Any] | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "createdAt",
        sort_order: str = "desc",
    ) -> dict[str, Any]:
        """Full-text search with filters and role-based visibility."""
        additional_filters: dict[str, Any] = {"schoolId": claims.school_id}

        if claims.has_any_role({Role.STUDENT, Role.PARENT}):
            additional_filters["status"] = MaterialStatus.PUBLISHED.value

        if filters:
            for key in ["gradeId", "subjectId", "termId", "unitId", "medium", "resourceType", "status"]:
                if filters.get(key):
                    additional_filters[key] = filters[key]

        items, total_count = await self._repo.text_search(
            search_query=search_query,
            additional_filters=additional_filters,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return {
            "items": items,
            "totalCount": total_count,
            "page": page,
            "pageSize": page_size,
            "totalPages": calc_total_pages(total_count, page_size),
        }

    async def update_material(
        self, material_id: str, update_data: dict[str, Any], claims: TokenClaims
    ) -> dict[str, Any]:
        """
        Partially update a material.
        Only DRAFT or PUBLISHED materials can be updated.
        """
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        if material.get("status") == MaterialStatus.ARCHIVED.value:
            raise LifecycleError("ARCHIVED", "UPDATE")

        # Scope check for teachers
        self._enforce_write_scope(material, claims)

        # Build $set payload — only include fields that are not None
        set_data: dict[str, Any] = {}
        field_map = {
            "title": "title",
            "description": "description",
            "subject_id": "subjectId",
            "grade_id": "gradeId",
            "term_id": "termId",
            "unit_id": "unitId",
            "medium": "medium",
            "resource_type": "resourceType",
            "tags": "tags",
            "file_id": "fileId",
            "external_url": "externalUrl",
            "thumbnail_url": "thumbnailUrl",
            "language": "language",
        }

        for py_key, db_key in field_map.items():
            if py_key in update_data and update_data[py_key] is not None:
                set_data[db_key] = update_data[py_key]

        if not set_data:
            return material  # Nothing to update

        set_data["updatedBy"] = claims.sub

        updated = await self._repo.update(material_id, set_data)
        if not updated:
            raise NotFoundError("Material", material_id)

        # Publish event
        event = material_events.material_updated(
            material_id, claims.sub, list(set_data.keys())
        )
        await self._publisher.publish(event)

        return updated

    async def soft_delete_material(
        self, material_id: str, claims: TokenClaims
    ) -> bool:
        """Archive/soft-delete a material."""
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        self._enforce_write_scope(material, claims)

        deleted = await self._repo.soft_delete(material_id, claims.sub)
        if not deleted:
            raise NotFoundError("Material", material_id)

        event = material_events.material_archived(material_id, claims.sub)
        await self._publisher.publish(event)

        return True

    # ── LIFECYCLE ─────────────────────────────────────────────

    async def publish_material(
        self, material_id: str, claims: TokenClaims
    ) -> dict[str, Any]:
        """
        Transition: DRAFT -> PUBLISHED.
        Validates minimum metadata completeness.
        """
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        current_status = material.get("status")
        if current_status == MaterialStatus.PUBLISHED.value:
            return material  # Idempotent

        if current_status != MaterialStatus.DRAFT.value:
            raise LifecycleError(current_status, MaterialStatus.PUBLISHED.value)

        # Completeness check
        missing = []
        for field in ["title", "subjectId", "gradeId", "resourceType"]:
            if not material.get(field):
                missing.append(field)

        # File/URL check
        resource_type = material.get("resourceType", "")
        if resource_type == ResourceType.LINK.value:
            if not material.get("externalUrl"):
                missing.append("externalUrl")
        elif not material.get("fileId") and not material.get("externalUrl"):
            missing.append("fileId or externalUrl")

        # Visibility check
        visibility = material.get("visibility", {})
        if not visibility.get("schoolId"):
            missing.append("visibility.schoolId")

        if missing:
            raise PublishValidationError(missing)

        now = datetime.utcnow()
        updated = await self._repo.update(material_id, {
            "status": MaterialStatus.PUBLISHED.value,
            "publishedAt": now,
            "publishedBy": claims.sub,
            "updatedBy": claims.sub,
        })

        event = material_events.material_published(material_id, claims.sub)
        await self._publisher.publish(event)

        return updated

    async def unpublish_material(
        self, material_id: str, claims: TokenClaims
    ) -> dict[str, Any]:
        """
        Transition: PUBLISHED -> DRAFT.
        """
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        current_status = material.get("status")
        if current_status == MaterialStatus.DRAFT.value:
            return material  # Idempotent

        if current_status != MaterialStatus.PUBLISHED.value:
            raise LifecycleError(current_status, MaterialStatus.DRAFT.value)

        updated = await self._repo.update(material_id, {
            "status": MaterialStatus.DRAFT.value,
            "updatedBy": claims.sub,
        })

        event = material_events.material_unpublished(material_id, claims.sub)
        await self._publisher.publish(event)

        return updated

    async def archive_material(
        self, material_id: str, claims: TokenClaims
    ) -> dict[str, Any]:
        """
        Transition: DRAFT|PUBLISHED -> ARCHIVED.
        """
        material = await self._repo.find_by_id(material_id)
        if not material:
            raise NotFoundError("Material", material_id)

        if material.get("schoolId") != claims.school_id:
            raise NotFoundError("Material", material_id)

        current_status = material.get("status")
        if current_status == MaterialStatus.ARCHIVED.value:
            return material  # Idempotent

        if current_status not in (MaterialStatus.DRAFT.value, MaterialStatus.PUBLISHED.value):
            raise LifecycleError(current_status, MaterialStatus.ARCHIVED.value)

        now = datetime.utcnow()
        updated = await self._repo.update(material_id, {
            "status": MaterialStatus.ARCHIVED.value,
            "archivedAt": now,
            "archivedBy": claims.sub,
            "updatedBy": claims.sub,
        })

        event = material_events.material_archived(material_id, claims.sub)
        await self._publisher.publish(event)

        return updated

    # ── HELPERS ────────────────────────────────────────────────

    def _enforce_write_scope(self, material: dict, claims: TokenClaims) -> None:
        """
        Enforce that the user has write access to this specific material
        based on their role and assigned scope.
        """
        if claims.is_admin_or_principal():
            return  # Full access

        if claims.has_role(Role.SUBJECT_TEACHER):
            # Can only modify materials for assigned subjects
            mat_subject = material.get("subjectId")
            if mat_subject and claims.subject_ids and mat_subject not in claims.subject_ids:
                raise AuthorizationError(
                    "You can only modify materials for your assigned subjects"
                )

        if claims.has_role(Role.SECTIONAL_HEAD):
            # Sectional heads can modify within their section scope
            return  # Simplified — full section resolution would need more data

        if claims.has_role(Role.CLASS_TEACHER):
            return  # Simplified — class teachers can modify their class materials
