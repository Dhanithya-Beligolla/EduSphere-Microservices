"""
group_core/responses.py
Standard response envelope used across all endpoints.
Matches the system-wide response shape defined in the system structure doc.
"""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

T = TypeVar("T")


class MetaSchema(BaseModel):
    requestId: str
    timestamp: str
    version: str = "v1"


class StandardResponse(BaseModel, Generic[T]):
    data: T | None = None
    meta: MetaSchema
    errors: list[str] = []

    @classmethod
    def success(cls, data: Any, version: str = "v1") -> "StandardResponse":
        return cls(
            data=data,
            meta=MetaSchema(
                requestId=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                version=version,
            ),
            errors=[],
        )

    @classmethod
    def error(cls, errors: list[str], version: str = "v1") -> "StandardResponse":
        return cls(
            data=None,
            meta=MetaSchema(
                requestId=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                version=version,
            ),
            errors=errors,
        )
