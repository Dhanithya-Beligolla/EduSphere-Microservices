"""
MongoDB connection lifecycle management.
Uses FastAPI lifespan to properly open and close the Motor client.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("db.mongo")

# Module-level references — set during lifespan, NOT at import time.
_client: AsyncIOMotorClient | None = None
_database: AsyncIOMotorDatabase | None = None


@asynccontextmanager
async def mongo_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Async context manager for MongoDB connection lifecycle.
    Opens the client on startup, closes on shutdown.
    """
    global _client, _database

    logger.info("connecting_to_mongodb", uri=settings.mongo_uri, db=settings.mongo_db_name)
    _client = AsyncIOMotorClient(settings.mongo_uri)
    _database = _client[settings.mongo_db_name]

    # Verify connectivity
    try:
        await _client.admin.command("ping")
        logger.info("mongodb_connected")
    except Exception as e:
        logger.error("mongodb_connection_failed", error=str(e))
        raise

    # Create indexes on startup
    from app.db.indexes import create_indexes
    await create_indexes(_database)

    yield

    # Shutdown
    logger.info("closing_mongodb_connection")
    _client.close()
    _client = None
    _database = None


def get_database() -> AsyncIOMotorDatabase:
    """
    Get the active database instance.
    Must be called after lifespan startup.
    """
    if _database is None:
        raise RuntimeError("Database not initialized. Ensure mongo_lifespan is running.")
    return _database
