"""
group_data/database.py
MongoDB connection and database initialization using Motor (async driver).
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

logger = logging.getLogger(__name__)

# Will be set on startup
db_client: AsyncIOMotorClient | None = None


async def connect_to_mongo(mongodb_url: str, db_name: str):
    """Create MongoDB connection and initialize Beanie ODM."""
    global db_client

    # Import all document models here
    from group_models.group_model import GroupDocument
    from group_models.membership_model import GroupMembershipDocument
    from group_models.activity_model import GroupActivityDocument
    from group_models.submission_model import GroupSubmissionDocument
    from group_models.peer_eval_model import PeerEvaluationDocument
    from group_models.result_model import GroupResultDocument

    logger.info(f"Connecting to MongoDB at {mongodb_url}, database: {db_name}")
    db_client = AsyncIOMotorClient(mongodb_url)
    database = db_client[db_name]

    await init_beanie(
        database=database,
        document_models=[
            GroupDocument,
            GroupMembershipDocument,
            GroupActivityDocument,
            GroupSubmissionDocument,
            PeerEvaluationDocument,
            GroupResultDocument,
        ],
    )
    logger.info("MongoDB connected and Beanie initialized.")


async def close_mongo_connection():
    """Close MongoDB connection."""
    global db_client
    if db_client:
        db_client.close()
        logger.info("MongoDB connection closed.")
