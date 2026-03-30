"""
Learning Material domain model — represents the MongoDB document structure.
"""

from datetime import datetime
from typing import Any


def new_learning_material(
    *,
    title: str,
    description: str | None = None,
    subject_id: str | None = None,
    grade_id: str | None = None,
    term_id: str | None = None,
    unit_id: str | None = None,
    medium: str | None = None,
    resource_type: str,
    tags: list[str] | None = None,
    visibility: dict[str, Any] | None = None,
    file_id: str | None = None,
    external_url: str | None = None,
    thumbnail_url: str | None = None,
    language: str | None = None,
    school_id: str,
    created_by: str,
) -> dict[str, Any]:
    """
    Factory function that builds a new learning material document
    ready for MongoDB insertion.
    """
    now = datetime.utcnow()

    return {
        "title": title,
        "description": description or "",
        "subjectId": subject_id,
        "gradeId": grade_id,
        "termId": term_id,
        "unitId": unit_id,
        "medium": medium,
        "resourceType": resource_type,
        "tags": tags or [],
        "status": "DRAFT",
        "visibility": visibility or {
            "scopeType": "SCHOOL",
            "schoolId": school_id,
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": [],
            "classIds": [],
            "subjectIds": [],
        },
        "currentVersion": 1,
        "fileId": file_id,
        "externalUrl": external_url,
        "thumbnailUrl": thumbnail_url,
        "language": language,
        "schoolId": school_id,
        "publishedAt": None,
        "publishedBy": None,
        "createdAt": now,
        "createdBy": created_by,
        "updatedAt": now,
        "updatedBy": created_by,
        "archivedAt": None,
        "archivedBy": None,
        "isDeleted": False,
    }
