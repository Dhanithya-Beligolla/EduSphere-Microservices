"""
Response builder helpers for the standard envelope.
"""

from datetime import datetime
from typing import Any

from app.schemas.common import ResponseEnvelope, Meta, ErrorDetail, PaginationMeta, PaginatedData


def make_response(
    data: Any,
    request_id: str,
    errors: list[ErrorDetail] | None = None,
) -> dict:
    """Build a standard response envelope dict."""
    return {
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "v1",
        },
        "errors": [e.model_dump(by_alias=True) for e in (errors or [])],
    }


def make_paginated_response(
    items: list[Any],
    total_count: int,
    page: int,
    page_size: int,
    total_pages: int,
    request_id: str,
) -> dict:
    """Build a paginated response envelope dict."""
    return {
        "data": {
            "items": items,
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "totalCount": total_count,
                "totalPages": total_pages,
            },
        },
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "v1",
        },
        "errors": [],
    }


def make_error_response(
    request_id: str,
    code: str,
    message: str,
    field: str | None = None,
) -> dict:
    """Build a single-error response envelope dict."""
    error = {"code": code, "message": message}
    if field:
        error["field"] = field
    return {
        "data": None,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "v1",
        },
        "errors": [error],
    }
