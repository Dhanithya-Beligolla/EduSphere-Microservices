from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..monitoring_models.monitoring_entities import (
    AuditLog,
    DashboardRecord,
    DashboardSnapshot,
    Intervention,
    KpiSnapshot,
    ReportRecord,
    RiskRule,
)
from .monitoring_mock_data import (
    ACADEMIC_RISK_REPORT,
    ASSIGNMENT_COMPLETION_REPORT,
    AUDIT_LOGS,
    CLASS_TEACHER_DASHBOARD,
    DASHBOARD_SNAPSHOTS,
    INTERVENTION_QUEUE,
    KPI_SNAPSHOTS,
    MATERIAL_USAGE_REPORT,
    PRINCIPAL_DASHBOARD,
    RISK_RULES,
    SECTIONAL_HEAD_DASHBOARD,
    SUBJECT_TEACHER_DASHBOARD,
)


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def seed_initial_data(db: Session) -> None:
    has_dashboards = db.query(func.count(DashboardRecord.id)).scalar() > 0
    if has_dashboards:
        return

    dashboard_records = [
        DashboardRecord(dashboard_type="principal", payload=PRINCIPAL_DASHBOARD),
        DashboardRecord(dashboard_type="sectional_head", payload=SECTIONAL_HEAD_DASHBOARD),
        DashboardRecord(dashboard_type="class_teacher", payload=CLASS_TEACHER_DASHBOARD),
        DashboardRecord(dashboard_type="subject_teacher", payload=SUBJECT_TEACHER_DASHBOARD),
    ]

    report_records = [
        ReportRecord(report_type="assignment_completion", payload=ASSIGNMENT_COMPLETION_REPORT),
        ReportRecord(report_type="academic_risk", payload=ACADEMIC_RISK_REPORT),
        ReportRecord(report_type="material_usage", payload=MATERIAL_USAGE_REPORT),
    ]

    risk_rules = [
        RiskRule(
            rule_id=item["ruleId"],
            name=item["name"],
            condition=item["condition"],
            risk_level=item["riskLevel"],
            active=item["active"],
            created_at=_parse_iso(item["createdAt"]),
        )
        for item in RISK_RULES
    ]

    audit_logs = [
        AuditLog(
            audit_id=item["auditId"],
            user_id=item["userId"],
            action=item["action"],
            resource=item["resource"],
            timestamp=_parse_iso(item["timestamp"]),
            ip_address=item["ipAddress"],
        )
        for item in AUDIT_LOGS
    ]

    kpi_snapshots = [
        KpiSnapshot(
            kpi_id=item["kpiId"],
            name=item["name"],
            value=item["value"],
            unit=item["unit"],
            trend=item["trend"],
            compared_to_previous_term=item["comparedToPreviousTerm"],
        )
        for item in KPI_SNAPSHOTS
    ]

    interventions = [
        Intervention(
            intervention_id=item["interventionId"],
            student_id=item["studentId"],
            class_id=item["classId"],
            reason=item["reason"],
            assigned_to=item["assignedTo"],
            status=item["status"],
            created_at=_parse_iso(item["createdAt"]),
            notes=item.get("notes"),
        )
        for item in INTERVENTION_QUEUE
    ]

    dashboard_snapshots = [
        DashboardSnapshot(
            snapshot_id=item["snapshotId"],
            role=item["role"],
            generated_at=_parse_iso(item["generatedAt"]),
            summary=item["summary"],
        )
        for item in DASHBOARD_SNAPSHOTS
    ]

    db.add_all(dashboard_records)
    db.add_all(report_records)
    db.add_all(risk_rules)
    db.add_all(audit_logs)
    db.add_all(kpi_snapshots)
    db.add_all(interventions)
    db.add_all(dashboard_snapshots)
    db.commit()
