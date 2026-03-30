"""
monitoring_reports.py
---------------------
Report, KPI, intervention, and snapshot endpoints for the Monitoring &
Administration Service. Covers assignment completion, academic risk,
material usage, async report-job queuing, KPI snapshots, the intervention
queue for at-risk students, and historical dashboard snapshots.
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse

# Relative imports from sibling packages
from ..monitoring_models.monitoring_schemas import (
    success,
    error,
    ReportJobRequest,
    InterventionUpdateRequest,
)
from ..monitoring_data.monitoring_mock_data import (
    ASSIGNMENT_COMPLETION_REPORT,
    ACADEMIC_RISK_REPORT,
    MATERIAL_USAGE_REPORT,
    REPORT_JOBS,
    KPI_SNAPSHOTS,
    INTERVENTION_QUEUE,
    DASHBOARD_SNAPSHOTS,
)

# ── Router setup ─────────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/api/v1",
    tags=["Reports"],
)


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
):
    """Return assignment completion totals for the given term."""
    data = {**ASSIGNMENT_COMPLETION_REPORT, "termId": termId}
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
):
    """Return at-risk students for the given grade."""
    data = {**ACADEMIC_RISK_REPORT, "gradeId": gradeId}
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
):
    """Return material usage statistics for the given subject."""
    data = {**MATERIAL_USAGE_REPORT, "subjectId": subjectId}
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
async def create_report_job(body: ReportJobRequest):
    """Queue an async report-export job and return the job ID."""
    job_id = f"RPT-{str(uuid4())[:4].upper()}"
    job = {
        "jobId": job_id,
        "reportType": body.reportType,
        "filters": body.filters,
        "format": body.format,
        "status": "QUEUED",
        "createdAt": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
    }
    # Store the job in the in-memory dict
    REPORT_JOBS[job_id] = job
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
async def get_report_job(jobId: str):
    """Return the status of an export job, or 404 if not found."""
    job = REPORT_JOBS.get(jobId)
    if not job:
        return JSONResponse(
            status_code=404,
            content=error(f"Report job '{jobId}' not found", "REPORT_JOB_NOT_FOUND"),
        )
    # Simulate completion
    job["status"] = "COMPLETED"
    job["downloadUrl"] = f"/api/v1/report-jobs/{jobId}/download"
    return success(job)


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
async def get_kpis():
    """Return all school-wide KPI snapshot records."""
    return success(KPI_SNAPSHOTS)


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
):
    """Return intervention records, optionally filtered by status."""
    if status:
        filtered = [i for i in INTERVENTION_QUEUE if i["status"] == status]
    else:
        filtered = INTERVENTION_QUEUE
    return success(filtered)


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
async def update_intervention(interventionId: str, body: InterventionUpdateRequest):
    """Update status / notes / assignedTo for an intervention."""
    # Find the intervention record
    for intervention in INTERVENTION_QUEUE:
        if intervention["interventionId"] == interventionId:
            intervention["status"] = body.status
            if body.notes is not None:
                intervention["notes"] = body.notes
            if body.assignedTo is not None:
                intervention["assignedTo"] = body.assignedTo
            return success(intervention)

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
async def get_snapshots():
    """Return all stored dashboard snapshots."""
    return success(DASHBOARD_SNAPSHOTS)
