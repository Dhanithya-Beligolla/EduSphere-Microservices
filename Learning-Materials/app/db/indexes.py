"""
MongoDB index definitions for the Learning Materials service.
Called once at startup to ensure indexes exist.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT

from app.core.logging import get_logger

logger = get_logger("db.indexes")


async def create_indexes(db: AsyncIOMotorDatabase) -> None:
    """Create all required indexes for the service collections."""

    logger.info("creating_indexes")

    # ── Learning Materials collection ──
    materials = db["learning_materials"]
    await materials.create_indexes([
        # Single field indexes for common filters
        IndexModel([("schoolId", ASCENDING)], name="idx_school_id"),
        IndexModel([("status", ASCENDING)], name="idx_status"),
        IndexModel([("gradeId", ASCENDING)], name="idx_grade_id"),
        IndexModel([("subjectId", ASCENDING)], name="idx_subject_id"),
        IndexModel([("termId", ASCENDING)], name="idx_term_id"),
        IndexModel([("medium", ASCENDING)], name="idx_medium"),
        IndexModel([("resourceType", ASCENDING)], name="idx_resource_type"),
        IndexModel([("tags", ASCENDING)], name="idx_tags"),
        IndexModel([("createdAt", DESCENDING)], name="idx_created_at"),
        IndexModel([("publishedAt", DESCENDING)], name="idx_published_at"),
        IndexModel([("isDeleted", ASCENDING)], name="idx_is_deleted"),

        # Compound indexes for frequent query patterns
        IndexModel(
            [("schoolId", ASCENDING), ("status", ASCENDING),
             ("gradeId", ASCENDING), ("subjectId", ASCENDING)],
            name="idx_school_status_grade_subject",
        ),
        IndexModel(
            [("schoolId", ASCENDING), ("status", ASCENDING),
             ("isDeleted", ASCENDING), ("createdAt", DESCENDING)],
            name="idx_school_status_deleted_created",
        ),
        IndexModel(
            [("visibility.scopeType", ASCENDING),
             ("visibility.classIds", ASCENDING)],
            name="idx_visibility_class",
        ),

        # Text index for free-text search on title, description, tags
        IndexModel(
            [("title", TEXT), ("description", TEXT), ("tags", TEXT)],
            name="idx_text_search",
            language_override="dummy_override",  # Ignore 'language' field since 'si', 'ta' aren't natively supported
        ),
    ])

    # ── Material Versions collection ──
    versions = db["material_versions"]
    await versions.create_indexes([
        IndexModel([("materialId", ASCENDING)], name="idx_material_id"),
        IndexModel(
            [("materialId", ASCENDING), ("versionNumber", ASCENDING)],
            name="idx_material_version",
            unique=True,
        ),
    ])

    logger.info("indexes_created")
