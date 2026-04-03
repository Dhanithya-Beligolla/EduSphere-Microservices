"""
monitoring_reports.py
---------------------
Report, KPI, intervention, and snapshot endpoints for the Monitoring &
Administration Service. Covers assignment completion, academic risk,
material usage, async report-job queuing, KPI snapshots, the intervention
queue for at-risk students, and historical dashboard snapshots.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Relative imports from sibling packages
from ..monitoring_models.monitoring_schemas import (
    success,
    error,
    ReportJobRequest,
    InterventionUpdateRequest,
)
from ..monitoring_core.database import get_db
from ..monitoring_models.monitoring_entities import (
    DashboardSnapshot,
    Intervention,
    KpiSnapshot,
    ReportJob,
    ReportRecord,
)

# ── Router setup ─────────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/api/v1",
    tags=["Reports"],
)


def _get_report_payload(db: Session, report_type: str) -> dict:
    record = db.query(ReportRecord).filter(ReportRecord.report_type == report_type).first()
    return record.payload if record else {}


def _job_to_dict(job: ReportJob) -> dict:
    return {
        "jobId": job.job_id,
        "reportType": job.report_type,
        "filters": job.filters,
        "format": job.format,
        "status": job.status,
        "createdAt": job.created_at.isoformat(),
        "downloadUrl": job.download_url,
    }


def _kpi_to_dict(item: KpiSnapshot) -> dict:
    return {
        "kpiId": item.kpi_id,
        "name": item.name,
        "value": item.value,
        "unit": item.unit,
        "trend": item.trend,
        "comparedToPreviousTerm": item.compared_to_previous_term,
    }


def _intervention_to_dict(item: Intervention) -> dict:
    return {
        "interventionId": item.intervention_id,
        "studentId": item.student_id,
        "classId": item.class_id,
        "reason": item.reason,
        "assignedTo": item.assigned_to,
        "status": item.status,
        "createdAt": item.created_at.isoformat(),
        "notes": item.notes,
    }


def _snapshot_to_dict(item: DashboardSnapshot) -> dict:
    return {
        "snapshotId": item.snapshot_id,
        "role": item.role,
        "generatedAt": item.generated_at.isoformat(),
        "summary": item.summary,
    }


# ── Assignment completion report ─────────────────────────────────────────────

@router.get(
    "/reports/assignment-completion",
    summary="Assignment completion report by grade and subject",
    description=(
        "Returns the assignment completion report for a given term. "
        "Includes totals grouped by grade (G07–G10) and by subject "
        "(SCI, MAT, ENG, HIS), along with overall completion rates."
    ),
)
async def get_assignment_completion_report(
    termId: str = Query(
        default="TERM-1",
        description="Term identifier, e.g. TERM-1, TERM-2, TERM-3",
    ),
    db: Session = Depends(get_db),
):
    """Return assignment completion totals for the given term."""
    base = _get_report_payload(db, "assignment_completion")
    data = {**base, "termId": termId}
    return success(data)


# ── Academic risk report ─────────────────────────────────────────────────────

@router.get(
    "/reports/academic-risk",
    summary="At-risk student report for a grade",
    description=(
        "Returns the list of academically at-risk students for a specific "
        "grade. Each student entry includes risk level (HIGH / MEDIUM), "
        "risk flags (LOW_SUBMISSION, LOW_SCORE, LOW_ATTENDANCE), and "
        "numeric indicators such as submission rate, average score, and "
        "attendance rate."
    ),
)
async def get_academic_risk_report(
    gradeId: str = Query(
        default="G09",
        description="Grade identifier, e.g. G07, G08, G09, G10",
    ),
    db: Session = Depends(get_db),
):
    """Return at-risk students for the given grade."""
    base = _get_report_payload(db, "academic_risk")
    data = {**base, "gradeId": gradeId}
    return success(data)


# ── Material usage report ────────────────────────────────────────────────────

@router.get(
    "/reports/material-usage",
    summary="Learning material usage statistics",
    description=(
        "Returns usage statistics for learning materials in a given subject. "
        "Includes top materials ranked by views/downloads, and a breakdown "
        "of total views/downloads by instruction medium (Sinhala, Tamil, "
        "English)."
    ),
)
async def get_material_usage_report(
    subjectId: str = Query(
        default="SCI",
        description="Subject identifier, e.g. SCI, MAT, ENG, HIS",
    ),
    db: Session = Depends(get_db),
):
    """Return material usage statistics for the given subject."""
    base = _get_report_payload(db, "material_usage")
    data = {**base, "subjectId": subjectId}
    return success(data)


# ── Report jobs (async export) ───────────────────────────────────────────────

@router.post(
    "/report-jobs",
    status_code=202,
    summary="Queue a background report export job (PDF or CSV)",
    description=(
        "Accepts a report export request and returns HTTP 202 Accepted. "
        "PDF / CSV generation happens asynchronously in the background. "
        "Use GET /report-jobs/{jobId} to poll for the result. The response "
        "contains the generated jobId and initial status (QUEUED)."
    ),
)
async def create_report_job(body: ReportJobRequest, db: Session = Depends(get_db)):
    """Queue an async report-export job and return the job ID."""
    job_id = f"RPT-{str(uuid4())[:4].upper()}"
    job = ReportJob(
        job_id=job_id,
        report_type=body.reportType,
        filters=body.filters or {},
        format=body.format,
        status="QUEUED",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(job)
    db.commit()
    return success({"jobId": job_id, "status": "QUEUED"})


@router.get(
    "/report-jobs/{jobId}",
    summary="Check export job status",
    description=(
        "Returns the current status of a previously queued report-export "
        "job. If the job exists, its status is advanced to COMPLETED and "
        "a downloadUrl is provided. Returns 404 if the jobId is unknown."
    ),
)
async def get_report_job(jobId: str, db: Session = Depends(get_db)):
    """Return the status of an export job, or 404 if not found."""
    job = db.query(ReportJob).filter(ReportJob.job_id == jobId).first()
    if not job:
        return JSONResponse(
            status_code=404,
            content=error(f"Report job '{jobId}' not found", "REPORT_JOB_NOT_FOUND"),
        )
    # Simulate completion
    job.status = "COMPLETED"
    job.download_url = f"/api/v1/report-jobs/{jobId}/download"
    job.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(job)
    return success(_job_to_dict(job))


# ── KPI snapshots ────────────────────────────────────────────────────────────

@router.get(
    "/kpis",
    summary="School-wide KPI snapshots",
    description=(
        "Returns the latest Key Performance Indicator snapshots for the "
        "whole school. Each KPI contains a name, current value, unit, "
        "trend direction (UP / DOWN / STABLE), and comparison against "
        "the previous term."
    ),
)
async def get_kpis(db: Session = Depends(get_db)):
    """Return all school-wide KPI snapshot records."""
    rows = db.query(KpiSnapshot).all()
    return success([_kpi_to_dict(item) for item in rows])


# ── Intervention queue ───────────────────────────────────────────────────────

@router.get(
    "/interventions",
    summary="Intervention queue for at-risk students",
    description=(
        "Returns the list of intervention records for at-risk students. "
        "Optionally filter by status (OPEN, IN_PROGRESS, RESOLVED, CLOSED). "
        "If no status filter is provided, all interventions are returned."
    ),
)
async def get_interventions(
    status: Optional[str] = Query(
        default=None,
        description="Filter by status: OPEN, IN_PROGRESS, RESOLVED, CLOSED",
    ),
    db: Session = Depends(get_db),
):
    """Return intervention records, optionally filtered by status."""
    query = db.query(Intervention)
    if status:
        query = query.filter(Intervention.status == status)
    rows = query.all()
    return success([_intervention_to_dict(item) for item in rows])


@router.patch(
    "/interventions/{interventionId}",
    summary="Update an intervention record",
    description=(
        "Partially updates an intervention record identified by "
        "interventionId. You can change the status, add case notes, "
        "or reassign the intervention to a different teacher. Returns "
        "the updated record or 404 if the interventionId is not found."
    ),
)
async def update_intervention(
    interventionId: str,
    body: InterventionUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update status / notes / assignedTo for an intervention."""
    # Find the intervention record
    intervention = (
        db.query(Intervention)
        .filter(Intervention.intervention_id == interventionId)
        .first()
    )
    if intervention:
        intervention.status = body.status
        if body.notes is not None:
            intervention.notes = body.notes
        if body.assignedTo is not None:
            intervention.assigned_to = body.assignedTo
        db.commit()
        db.refresh(intervention)
        return success(_intervention_to_dict(intervention))

    # Not found
    return JSONResponse(
        status_code=404,
        content=error(
            f"Intervention '{interventionId}' not found",
            "INTERVENTION_NOT_FOUND",
        ),
    )


# ── Dashboard snapshots ─────────────────────────────────────────────────────

@router.get(
    "/snapshots",
    summary="List recent dashboard snapshots",
    description=(
        "Returns a list of periodically generated dashboard snapshots. "
        "Each snapshot captures the key metrics for a given role "
        "(PRINCIPAL, SECTIONAL_HEAD, CLASS_TEACHER) at a specific point "
        "in time."
    ),
)
async def get_snapshots(db: Session = Depends(get_db)):
    """Return all stored dashboard snapshots."""
    rows = db.query(DashboardSnapshot).all()
    return success([_snapshot_to_dict(item) for item in rows])
