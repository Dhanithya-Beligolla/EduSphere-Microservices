"""
monitoring_risk_audit.py
------------------------
Risk rule management and audit-trail endpoints for the Monitoring &
Administration Service. Risk rules drive automated at-risk student
detection; audit logs provide a tamper-evident trail of user actions.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response

# Relative imports from sibling packages
from ..monitoring_models.monitoring_schemas import success, error, RiskRuleRequest
from ..monitoring_data.monitoring_mock_data import RISK_RULES, AUDIT_LOGS

# ── Router setup ─────────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/api/v1",
    tags=["Risk Rules & Audit"],
)


# ── Risk Rules ───────────────────────────────────────────────────────────────

@router.get(
    "/risk-rules",
    summary="List all configured risk rules",
    description=(
        "Returns every risk-detection rule currently stored in the system. "
        "Each rule has a human-readable name, a condition expression "
        "(e.g. 'submissionRate < 60'), a risk level, and an active flag."
    ),
)
async def list_risk_rules():
    """Return all risk rules (active and inactive)."""
    return success(RISK_RULES)


@router.post(
    "/risk-rules",
    status_code=201,
    summary="Create a new student risk detection rule",
    description=(
        "Creates and stores a new risk-detection rule. Conditions use a "
        "simple 'field operator value' syntax — for example: "
        "'avgScore < 50', 'submissionRate < 60', 'attendanceRate < 70'. "
        "The rule is immediately active unless active=false is supplied."
    ),
)
async def create_risk_rule(body: RiskRuleRequest):
    """Create a new risk rule and append it to the list."""
    rule = {
        "ruleId": f"RR-{str(uuid4())[:3].upper()}",
        "name": body.name,
        "condition": body.condition,
        "riskLevel": body.riskLevel,
        "active": body.active,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    RISK_RULES.append(rule)
    return success(rule)


@router.delete(
    "/risk-rules/{ruleId}",
    status_code=204,
    summary="Deactivate a risk rule",
    description=(
        "Soft-deletes a risk rule by setting its active flag to False. "
        "The rule remains in the list for audit purposes but will no "
        "longer trigger risk detection. Returns 204 No Content on success "
        "or 404 if the ruleId is not found."
    ),
)
async def deactivate_risk_rule(ruleId: str):
    """Set active=False for the given rule, or 404 if not found."""
    for rule in RISK_RULES:
        if rule["ruleId"] == ruleId:
            rule["active"] = False
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content=error(f"Risk rule '{ruleId}' not found", "RISK_RULE_NOT_FOUND"),
    )


# ── Audit Logs ───────────────────────────────────────────────────────────────

@router.get(
    "/audit-views/user-activity",
    summary="View audit trail for a specific user",
    description=(
        "Returns the audit trail filtered by userId. Each entry contains "
        "the action performed (e.g. CREATE_ASSIGNMENT, GRADE_SUBMISSION), "
        "the resource affected, a timestamp, and the originating IP address."
    ),
)
async def get_user_activity(
    userId: str = Query(
        default="TCH-230",
        description="User identifier to filter audit logs, e.g. TCH-230",
    ),
):
    """Return audit log entries for a specific user."""
    filtered = [log for log in AUDIT_LOGS if log["userId"] == userId]
    return success(filtered)


@router.post(
    "/audit-views",
    status_code=201,
    summary="Log a new audit entry",
    description=(
        "Appends a new audit-trail entry. The request body must contain "
        "userId, action, and resource. The server automatically assigns "
        "an auditId and timestamp."
    ),
)
async def create_audit_entry(body: dict):
    """Create a new audit log entry from the supplied dict."""
    entry = {
        "auditId": f"AUD-{str(uuid4())[:4].upper()}",
        "userId": body.get("userId", "UNKNOWN"),
        "action": body.get("action", "UNKNOWN"),
        "resource": body.get("resource", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ipAddress": "0.0.0.0",  # placeholder for mock
    }
    AUDIT_LOGS.append(entry)
    return success(entry)
