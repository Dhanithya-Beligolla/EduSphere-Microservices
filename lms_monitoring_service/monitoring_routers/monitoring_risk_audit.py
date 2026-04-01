"""
monitoring_risk_audit.py
------------------------
Risk rule management and audit-trail endpoints for the Monitoring &
Administration Service. Risk rules drive automated at-risk student
detection; audit logs provide a tamper-evident trail of user actions.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

# Relative imports from sibling packages
from ..monitoring_models.monitoring_schemas import success, error, RiskRuleRequest
from ..monitoring_core.database import get_db
from ..monitoring_models.monitoring_entities import AuditLog, RiskRule

# ── Router setup ─────────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/api/v1",
    tags=["Risk Rules & Audit"],
)


def _risk_rule_to_dict(rule: RiskRule) -> dict:
    return {
        "ruleId": rule.rule_id,
        "name": rule.name,
        "condition": rule.condition,
        "riskLevel": rule.risk_level,
        "active": rule.active,
        "createdAt": rule.created_at.isoformat(),
    }


def _audit_to_dict(item: AuditLog) -> dict:
    return {
        "auditId": item.audit_id,
        "userId": item.user_id,
        "action": item.action,
        "resource": item.resource,
        "timestamp": item.timestamp.isoformat(),
        "ipAddress": item.ip_address,
    }


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
async def list_risk_rules(db: Session = Depends(get_db)):
    """Return all risk rules (active and inactive)."""
    rows = db.query(RiskRule).all()
    return success([_risk_rule_to_dict(rule) for rule in rows])


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
async def create_risk_rule(body: RiskRuleRequest, db: Session = Depends(get_db)):
    """Create a new risk rule and append it to the list."""
    rule = RiskRule(
        rule_id=f"RR-{str(uuid4())[:3].upper()}",
        name=body.name,
        condition=body.condition,
        risk_level=body.riskLevel,
        active=body.active,
        created_at=datetime.now(timezone.utc),
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return success(_risk_rule_to_dict(rule))


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
async def deactivate_risk_rule(ruleId: str, db: Session = Depends(get_db)):
    """Set active=False for the given rule, or 404 if not found."""
    rule = db.query(RiskRule).filter(RiskRule.rule_id == ruleId).first()
    if rule:
        rule.active = False
        db.commit()
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
    db: Session = Depends(get_db),
):
    """Return audit log entries for a specific user."""
    logs = db.query(AuditLog).filter(AuditLog.user_id == userId).all()
    return success([_audit_to_dict(item) for item in logs])


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
async def create_audit_entry(body: dict, db: Session = Depends(get_db)):
    """Create a new audit log entry from the supplied dict."""
    entry = AuditLog(
        audit_id=f"AUD-{str(uuid4())[:4].upper()}",
        user_id=body.get("userId", "UNKNOWN"),
        action=body.get("action", "UNKNOWN"),
        resource=body.get("resource", ""),
        timestamp=datetime.now(timezone.utc),
        ip_address=body.get("ipAddress", "0.0.0.0"),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return success(_audit_to_dict(entry))
