"""
MongoDB repository for material versions.
"""

from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING

from app.db.mongo import get_database
from app.utils.object_id import to_object_id, serialize_doc, serialize_docs
from app.core.logging import get_logger

logger = get_logger("repositories.version")

COLLECTION = "material_versions"


class VersionRepository:
    """Async MongoDB repository for material version documents."""

    def __init__(self, db: AsyncIOMotorDatabase | None = None):
        self._db = db

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return self._db or get_database()

    @property
    def collection(self):
        return self.db[COLLECTION]

    async def create(self, document: dict[str, Any]) -> str:
        """Insert a new version document. Returns inserted ID as string."""
        result = await self.collection.insert_one(document)
        logger.info(
            "version_created",
            version_id=str(result.inserted_id),
            material_id=document.get("materialId"),
            version_number=document.get("versionNumber"),
        )
        return str(result.inserted_id)

    async def find_by_material_id(self, material_id: str) -> list[dict]:
        """Find all versions for a material, sorted ascending by version number."""
        cursor = (
            self.collection
            .find({"materialId": material_id})
            .sort("versionNumber", ASCENDING)
        )
        docs = await cursor.to_list(length=1000)
        return serialize_docs(docs)

    async def find_by_version_number(
        self, material_id: str, version_number: int
    ) -> dict | None:
        """Find a specific version by material ID and version number."""
        doc = await self.collection.find_one({
            "materialId": material_id,
            "versionNumber": version_number,
        })
        return serialize_doc(doc) if doc else None

    async def get_latest_version_number(self, material_id: str) -> int:
        """Get the highest version number for a material. Returns 0 if none exist."""
        cursor = (
            self.collection
            .find({"materialId": material_id})
            .sort("versionNumber", -1)
            .limit(1)
        )
        docs = await cursor.to_list(length=1)
        if docs:
            return docs[0].get("versionNumber", 0)
        return 0
