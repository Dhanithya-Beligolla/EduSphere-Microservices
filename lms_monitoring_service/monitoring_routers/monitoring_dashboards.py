"""
monitoring_dashboards.py
------------------------
Role-based dashboard endpoints for the Monitoring & Administration Service.
Each dashboard returns aggregated, read-only data tailored to a specific
school role: Principal, Sectional Head, Class Teacher, or Subject Teacher.
"""

from fastapi import APIRouter, Query

# Relative imports from sibling packages
from ..monitoring_models.monitoring_schemas import success
from ..monitoring_data.monitoring_mock_data import (
    PRINCIPAL_DASHBOARD,
    SECTIONAL_HEAD_DASHBOARD,
    CLASS_TEACHER_DASHBOARD,
    SUBJECT_TEACHER_DASHBOARD,
)

# ── Router setup ─────────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/api/v1/dashboards",
    tags=["Dashboards"],
)


# ── Principal Dashboard ─────────────────────────────────────────────────────

@router.get(
    "/principal",
    summary="Whole-school dashboard for Principal",
    description=(
        "Returns the full school-wide Key Performance Indicators (KPIs) "
        "for the Principal. This includes total student/teacher counts, "
        "overall attendance rate, the number of at-risk students, "
        "per-section performance breakdowns (Primary, Junior Secondary, "
        "Senior Secondary, Advanced Level), and recent system alerts. "
        "The Principal role has visibility over the entire school."
    ),
)
async def get_principal_dashboard():
    """Return whole-school KPIs for the Principal."""
    return success(PRINCIPAL_DASHBOARD)


# ── Sectional Head Dashboard ────────────────────────────────────────────────

@router.get(
    "/sectional-head",
    summary="Section dashboard for Sectional Head",
    description=(
        "Returns a filtered dashboard scoped to a specific section of the "
        "school. Sectional Heads only see their assigned section (e.g. "
        "SEC-JUNIOR for Junior Secondary G6–G9). The response includes "
        "the class list with teacher assignments, attendance and submission "
        "rates per class, teacher activity metrics, and a list of at-risk "
        "students within that section."
    ),
)
async def get_sectional_head_dashboard(
    sectionId: str = Query(
        default="SEC-JUNIOR",
        description="Section identifier, e.g. SEC-PRIMARY, SEC-JUNIOR, SEC-SENIOR, SEC-AL",
    ),
):
    """Return section-level KPIs for a Sectional Head."""
    # Clone the mock data and update the sectionId to reflect the query param
    data = {**SECTIONAL_HEAD_DASHBOARD, "sectionId": sectionId}
    return success(data)


# ── Class Teacher Dashboard ─────────────────────────────────────────────────

@router.get(
    "/class-teacher",
    summary="Class dashboard for Class Teacher",
    description=(
        "Returns a dashboard scoped to a single class. Class Teachers see "
        "only their assigned class (e.g. CLS-G09-A). The response includes "
        "per-subject progress (avg score, submission rate, topic completion), "
        "weekly attendance trends, and student highlights (top performer and "
        "students needing attention)."
    ),
)
async def get_class_teacher_dashboard(
    classId: str = Query(
        default="CLS-G09-A",
        description="Class identifier, e.g. CLS-G09-A",
    ),
):
    """Return class-level KPIs for a Class Teacher."""
    data = {**CLASS_TEACHER_DASHBOARD, "classId": classId}
    return success(data)


# ── Subject Teacher Dashboard ───────────────────────────────────────────────

@router.get(
    "/subject-teacher",
    summary="Subject-level dashboard for Subject Teacher",
    description=(
        "Returns a dashboard scoped to a specific subject in a specific "
        "class. Subject Teachers see only their assigned classes and "
        "subjects (e.g. Science in CLS-G09-A). The response includes "
        "assignment statistics (total, published, drafts), per-assignment "
        "submission rates, grade distribution, and ranked lists of top "
        "and bottom-performing students."
    ),
)
async def get_subject_teacher_dashboard(
    classId: str = Query(
        default="CLS-G09-A",
        description="Class identifier, e.g. CLS-G09-A",
    ),
    subjectId: str = Query(
        default="SCI",
        description="Subject identifier, e.g. SCI, MAT, ENG, HIS",
    ),
):
    """Return subject-level KPIs for a Subject Teacher."""
    data = {
        **SUBJECT_TEACHER_DASHBOARD,
        "classId": classId,
        "subjectId": subjectId,
    }
    return success(data)
