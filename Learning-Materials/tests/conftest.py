"""
Shared pytest fixtures for the Learning Materials test suite.
Provides: test app, async client, mock DB, and token factory.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import jwt
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.core.config import settings


def create_test_token(
    sub: str = "teacher-001",
    school_id: str = "school-001",
    roles: list[str] | None = None,
    subject_ids: list[str] | None = None,
    class_ids: list[str] | None = None,
    section_ids: list[str] | None = None,
    stream_ids: list[str] | None = None,
    permissions: list[str] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT token for testing.
    """
    payload = {
        "sub": sub,
        "school_id": school_id,
        "roles": roles or ["SUBJECT_TEACHER"],
        "subject_ids": subject_ids or ["subject-science"],
        "class_ids": class_ids or ["class-9a"],
        "section_ids": section_ids or [],
        "stream_ids": stream_ids or [],
        "permissions": permissions or [],
        "exp": datetime.utcnow() + (expires_delta or timedelta(hours=1)),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


# Pre-built tokens for common test scenarios
TEACHER_TOKEN = create_test_token()

ADMIN_TOKEN = create_test_token(
    sub="admin-001",
    roles=["ADMIN"],
    subject_ids=[],
    class_ids=[],
)

PRINCIPAL_TOKEN = create_test_token(
    sub="principal-001",
    roles=["PRINCIPAL"],
    subject_ids=[],
    class_ids=[],
)

STUDENT_TOKEN = create_test_token(
    sub="student-001",
    roles=["STUDENT"],
    subject_ids=["subject-science"],
    class_ids=["class-9a"],
)

PARENT_TOKEN = create_test_token(
    sub="parent-001",
    roles=["PARENT"],
    subject_ids=[],
    class_ids=["class-9a"],
)


# ── Mock MongoDB ──────────────────────────────────────────────

class MockCollection:
    """In-memory mock MongoDB collection for testing."""

    def __init__(self):
        self._docs: list[dict] = []
        self._id_counter = 0

    def _next_id(self):
        self._id_counter += 1
        from bson import ObjectId
        return ObjectId()

    async def insert_one(self, doc: dict) -> MagicMock:
        doc = dict(doc)
        if "_id" not in doc:
            doc["_id"] = self._next_id()
        self._docs.append(doc)
        result = MagicMock()
        result.inserted_id = doc["_id"]
        return result

    def find(self, filter_query: dict | None = None):
        docs = self._filter(filter_query or {})
        return MockCursor(docs)

    async def find_one(self, filter_query: dict) -> dict | None:
        docs = self._filter(filter_query)
        return docs[0] if docs else None

    async def find_one_and_update(
        self, filter_query: dict, update: dict, return_document: bool = False
    ) -> dict | None:
        docs = self._filter(filter_query)
        if not docs:
            return None
        doc = docs[0]
        if "$set" in update:
            doc.update(update["$set"])
        return doc

    async def update_one(self, filter_query: dict, update: dict) -> MagicMock:
        docs = self._filter(filter_query)
        result = MagicMock()
        if docs:
            doc = docs[0]
            if "$set" in update:
                doc.update(update["$set"])
            result.modified_count = 1
        else:
            result.modified_count = 0
        return result

    async def count_documents(self, filter_query: dict) -> int:
        return len(self._filter(filter_query))

    async def create_indexes(self, indexes):
        pass  # No-op in tests

    def _filter(self, query: dict) -> list[dict]:
        results = []
        for doc in self._docs:
            match = True
            for key, value in query.items():
                if key == "$text":
                    # Simple text search mock
                    search_term = value.get("$search", "").lower()
                    combined = f"{doc.get('title', '')} {doc.get('description', '')} {' '.join(doc.get('tags', []))}".lower()
                    if search_term and search_term not in combined:
                        match = False
                elif key == "_id":
                    if doc.get("_id") != value:
                        match = False
                elif isinstance(value, dict):
                    if "$in" in value:
                        doc_val = doc.get(key)
                        if isinstance(doc_val, list):
                            if not any(v in doc_val for v in value["$in"]):
                                match = False
                        elif doc_val not in value["$in"]:
                            match = False
                else:
                    # Dot notation support for nested fields
                    if "." in key:
                        parts = key.split(".")
                        val = doc
                        for part in parts:
                            if isinstance(val, dict):
                                val = val.get(part)
                            else:
                                val = None
                                break
                        if val != value:
                            match = False
                    elif doc.get(key) != value:
                        match = False
            if match:
                results.append(doc)
        return results


class MockCursor:
    """Mock async cursor for MongoDB find operations."""

    def __init__(self, docs: list[dict]):
        self._docs = docs
        self._sort_key = None
        self._sort_dir = 1
        self._skip = 0
        self._limit_val = None

    def sort(self, key, direction=1):
        self._sort_key = key
        self._sort_dir = direction
        return self

    def skip(self, n: int):
        self._skip = n
        return self

    def limit(self, n: int):
        self._limit_val = n
        return self

    async def to_list(self, length: int = 100) -> list[dict]:
        docs = list(self._docs)
        if self._sort_key:
            reverse = self._sort_dir == -1
            docs.sort(key=lambda d: d.get(self._sort_key, ""), reverse=reverse)
        docs = docs[self._skip:]
        limit = self._limit_val or length
        return docs[:limit]


class MockDatabase:
    """Mock async MongoDB database."""

    def __init__(self):
        self._collections: dict[str, MockCollection] = {}

    def __getitem__(self, name: str) -> MockCollection:
        if name not in self._collections:
            self._collections[name] = MockCollection()
        return self._collections[name]

    async def command(self, cmd: str):
        return {"ok": 1}


# ── Fixtures ──────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    """Provide a fresh mock database for each test."""
    return MockDatabase()


@pytest_asyncio.fixture
async def client(mock_db) -> AsyncGenerator[AsyncClient, None]:
    """
    Provide an async test client with mocked MongoDB.
    """
    with patch("app.db.mongo.get_database", return_value=mock_db):
        with patch("app.db.mongo._database", mock_db):
            # Import app after patching to ensure routes use mock DB
            from app.main import app

            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport,
                base_url="http://test",
            ) as ac:
                yield ac
