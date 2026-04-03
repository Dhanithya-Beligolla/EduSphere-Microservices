"""
monitoring_schemas.py
---------------------
Pydantic v2 request / response models and standard response helpers.
Every endpoint in the Monitoring & Administration Service returns the
standard shape: {"data": ..., "meta": {...}, "errors": [...]}.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


# ── Standard response helpers ────────────────────────────────────────────────

def make_meta() -> dict:
    """Build the common *meta* block included in every API response."""
    return {
        "requestId": str(uuid4())[:8],           # short unique id per request
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "v1"
    }


def success(data) -> dict:
    """Wrap *data* in the standard success envelope."""
    return {
        "data": data,
        "meta": make_meta(),
        "errors": []
    }


def error(message: str, code: str) -> dict:
    """Build a standard error envelope."""
    return {
        "data": None,
        "meta": make_meta(),
        "errors": [{"message": message, "code": code}]
    }


# ── Request models ───────────────────────────────────────────────────────────

class ReportJobRequest(BaseModel):
    """Body for POST /report-jobs — queue an async report export."""
    reportType: str                         # e.g. "ASSIGNMENT_COMPLETION"
    filters: Optional[dict] = {}            # optional filter criteria
    format: str = "PDF"                     # PDF or CSV


class RiskRuleRequest(BaseModel):
    """Body for POST /risk-rules — create a new automated risk rule."""
    name: str                               # human-readable rule name
    condition: str                          # e.g. "submissionRate < 60"
    riskLevel: str                          # HIGH, MEDIUM, LOW
    active: bool = True                     # default to enabled


class InterventionUpdateRequest(BaseModel):
    """Body for PATCH /interventions/{interventionId}."""
    status: str                             # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    notes: Optional[str] = None             # optional case notes
    assignedTo: Optional[str] = None        # reassign to another teacher
