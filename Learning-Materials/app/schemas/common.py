"""
Common response envelope and error schemas.
Every API response is wrapped in a ResponseEnvelope for consistency.
"""

from datetime import datetime
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class Meta(BaseModel):
    """Response metadata attached to every envelope."""
    request_id: str = Field(..., alias="requestId")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: str = "v1"

    model_config = {"populate_by_name": True}


class ErrorDetail(BaseModel):
    """Single error entry in the envelope."""
    code: str
    message: str
    field: str | None = None


class ResponseEnvelope(BaseModel, Generic[T]):
    """Standard JSON response envelope."""
    data: T | None = None
    meta: Meta
    errors: list[ErrorDetail] = Field(default_factory=list)


class PaginationMeta(BaseModel):
    """Pagination metadata for list responses."""
    page: int
    page_size: int = Field(..., alias="pageSize")
    total_count: int = Field(..., alias="totalCount")
    total_pages: int = Field(..., alias="totalPages")

    model_config = {"populate_by_name": True}


class PaginatedData(BaseModel, Generic[T]):
    """Wrapper for paginated list data."""
    items: list[Any] = Field(default_factory=list)
    pagination: PaginationMeta
