"""
MongoDB repository for learning materials.
Isolates all database queries — no business logic here.
"""

from datetime import datetime
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING

from app.db.mongo import get_database
from app.utils.object_id import to_object_id, serialize_doc, serialize_docs
from app.utils.pagination import calc_skip
from app.core.logging import get_logger

logger = get_logger("repositories.material")

COLLECTION = "learning_materials"


class MaterialRepository:
    """Async MongoDB repository for learning material documents."""

    def __init__(self, db: AsyncIOMotorDatabase | None = None):
        self._db = db

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return self._db or get_database()

    @property
    def collection(self):
        return self.db[COLLECTION]

    async def create(self, document: dict[str, Any]) -> str:
        """Insert a new material document. Returns the inserted ID as string."""
        result = await self.collection.insert_one(document)
        logger.info("material_created", material_id=str(result.inserted_id))
        return str(result.inserted_id)

    async def find_by_id(self, material_id: str, include_deleted: bool = False) -> dict | None:
        """Find a single material by ID. Returns None if not found."""
        query: dict[str, Any] = {"_id": to_object_id(material_id)}
        if not include_deleted:
            query["isDeleted"] = False
        doc = await self.collection.find_one(query)
        return serialize_doc(doc) if doc else None

    async def find_many(
        self,
        filter_query: dict[str, Any],
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "createdAt",
        sort_order: str = "desc",
    ) -> tuple[list[dict], int]:
        """
        Find materials matching the filter, with pagination and sorting.
        Returns (items, total_count).
        """
        # Always exclude soft-deleted unless filter explicitly includes them
        if "isDeleted" not in filter_query:
            filter_query["isDeleted"] = False

        sort_direction = DESCENDING if sort_order == "desc" else ASCENDING
        skip = calc_skip(page, page_size)

        cursor = (
            self.collection
            .find(filter_query)
            .sort(sort_by, sort_direction)
            .skip(skip)
            .limit(page_size)
        )

        docs = await cursor.to_list(length=page_size)
        total_count = await self.collection.count_documents(filter_query)

        return serialize_docs(docs), total_count

    async def text_search(
        self,
        search_query: str,
        additional_filters: dict[str, Any] | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "createdAt",
        sort_order: str = "desc",
    ) -> tuple[list[dict], int]:
        """
        Full-text search on title, description, and tags.
        Falls back to regex if text search fails.
        """
        filter_query: dict[str, Any] = {"isDeleted": False}

        if additional_filters:
            filter_query.update(additional_filters)

        if search_query:
            filter_query["$text"] = {"$search": search_query}

        return await self.find_many(
            filter_query=filter_query,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def update(self, material_id: str, update_data: dict[str, Any]) -> dict | None:
        """
        Partially update a material document.
        update_data should NOT include _id.
        Returns the updated document or None.
        """
        update_data["updatedAt"] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            {"_id": to_object_id(material_id), "isDeleted": False},
            {"$set": update_data},
            return_document=True,
        )
        if result:
            logger.info("material_updated", material_id=material_id)
        return serialize_doc(result) if result else None

    async def soft_delete(self, material_id: str, deleted_by: str) -> bool:
        """Mark a material as soft-deleted."""
        result = await self.collection.update_one(
            {"_id": to_object_id(material_id), "isDeleted": False},
            {
                "$set": {
                    "isDeleted": True,
                    "updatedAt": datetime.utcnow(),
                    "updatedBy": deleted_by,
                }
            },
        )
        if result.modified_count > 0:
            logger.info("material_soft_deleted", material_id=material_id)
            return True
        return False

    async def count(self, filter_query: dict[str, Any] | None = None) -> int:
        """Count documents matching a filter."""
        query = filter_query or {}
        if "isDeleted" not in query:
            query["isDeleted"] = False
        return await self.collection.count_documents(query)
