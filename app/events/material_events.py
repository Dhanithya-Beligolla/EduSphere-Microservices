"""
Typed domain events for the Learning Materials service.
"""

from app.events.base import DomainEvent


def material_created(material_id: str, created_by: str, title: str) -> DomainEvent:
    return DomainEvent(
        event_type="content.material.created",
        aggregate_id=material_id,
        payload={"createdBy": created_by, "title": title},
    )


def material_updated(material_id: str, updated_by: str, changed_fields: list[str]) -> DomainEvent:
    return DomainEvent(
        event_type="content.material.updated",
        aggregate_id=material_id,
        payload={"updatedBy": updated_by, "changedFields": changed_fields},
    )


def material_published(material_id: str, published_by: str) -> DomainEvent:
    return DomainEvent(
        event_type="content.material.published",
        aggregate_id=material_id,
        payload={"publishedBy": published_by},
    )


def material_unpublished(material_id: str, unpublished_by: str) -> DomainEvent:
    return DomainEvent(
        event_type="content.material.unpublished",
        aggregate_id=material_id,
        payload={"unpublishedBy": unpublished_by},
    )


def material_archived(material_id: str, archived_by: str) -> DomainEvent:
    return DomainEvent(
        event_type="content.material.archived",
        aggregate_id=material_id,
        payload={"archivedBy": archived_by},
    )


def material_versioned(material_id: str, version_number: int, created_by: str) -> DomainEvent:
    return DomainEvent(
        event_type="content.material.versioned",
        aggregate_id=material_id,
        payload={"versionNumber": version_number, "createdBy": created_by},
    )
