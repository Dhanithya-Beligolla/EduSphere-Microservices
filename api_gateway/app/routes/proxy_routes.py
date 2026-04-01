from typing import Any

from fastapi import APIRouter, Request

from app.controllers.gateway_controller import proxy_to_service
from app.core.constants import HTTP_METHODS

router = APIRouter(tags=["Service Proxy"])


def _proxy_handler_factory(service_key: str, upstream_template: str):
    async def _handler(request: Request):
        path_params: dict[str, Any] = dict(request.path_params)
        upstream_path = upstream_template.format(**path_params)
        return await proxy_to_service(request, service_key, upstream_path)

    return _handler


# Documented proxy operations grouped by service so Swagger shows a complete gateway catalog.
DOCUMENTED_PROXY_ROUTES = [
    # Identity
    ("GET", "/identity/health", "identity", "health", "Identity Health", "Identity Service (Proxy)"),
    ("POST", "/identity/api/v1/auth/login", "identity", "api/v1/auth/login", "Identity Login", "Identity Service (Proxy)"),
    ("POST", "/identity/api/v1/auth/register", "identity", "api/v1/auth/register", "Identity Register User", "Identity Service (Proxy)"),
    ("GET", "/identity/api/v1/auth/me", "identity", "api/v1/auth/me", "Identity Current User", "Identity Service (Proxy)"),
    ("GET", "/identity/api/v1/auth/verify", "identity", "api/v1/auth/verify", "Identity Verify Token", "Identity Service (Proxy)"),
    ("GET", "/identity/api/v1/auth/users", "identity", "api/v1/auth/users", "Identity List Users", "Identity Service (Proxy)"),
    ("GET", "/identity/api/v1/auth/users/{userId}", "identity", "api/v1/auth/users/{userId}", "Identity Get User", "Identity Service (Proxy)"),
    ("PATCH", "/identity/api/v1/auth/users/{userId}/status", "identity", "api/v1/auth/users/{userId}/status", "Identity Update User Status", "Identity Service (Proxy)"),
    # Academic
    ("GET", "/academic/api/health", "academic", "api/health", "Academic Health", "Academic Service (Proxy)"),
    ("GET", "/academic/api/academic-years", "academic", "api/academic-years", "Academic List Years", "Academic Service (Proxy)"),
    ("GET", "/academic/api/academic-years/active", "academic", "api/academic-years/active", "Academic Active Year", "Academic Service (Proxy)"),
    ("POST", "/academic/api/academic-years", "academic", "api/academic-years", "Academic Create Year", "Academic Service (Proxy)"),
    ("PATCH", "/academic/api/academic-years/{academicYearId}/activate", "academic", "api/academic-years/{academicYearId}/activate", "Academic Activate Year", "Academic Service (Proxy)"),
    ("DELETE", "/academic/api/academic-years/{academicYearId}", "academic", "api/academic-years/{academicYearId}", "Academic Delete Year", "Academic Service (Proxy)"),
    ("GET", "/academic/api/grades", "academic", "api/grades", "Academic List Grades", "Academic Service (Proxy)"),
    ("POST", "/academic/api/grades", "academic", "api/grades", "Academic Create Grade", "Academic Service (Proxy)"),
    ("PUT", "/academic/api/grades/{gradeId}", "academic", "api/grades/{gradeId}", "Academic Update Grade", "Academic Service (Proxy)"),
    ("DELETE", "/academic/api/grades/{gradeId}", "academic", "api/grades/{gradeId}", "Academic Delete Grade", "Academic Service (Proxy)"),
    ("GET", "/academic/api/sections", "academic", "api/sections", "Academic List Sections", "Academic Service (Proxy)"),
    ("POST", "/academic/api/sections", "academic", "api/sections", "Academic Create Section", "Academic Service (Proxy)"),
    ("PUT", "/academic/api/sections/{sectionId}", "academic", "api/sections/{sectionId}", "Academic Update Section", "Academic Service (Proxy)"),
    ("DELETE", "/academic/api/sections/{sectionId}", "academic", "api/sections/{sectionId}", "Academic Delete Section", "Academic Service (Proxy)"),
    ("GET", "/academic/api/subjects", "academic", "api/subjects", "Academic List Subjects", "Academic Service (Proxy)"),
    ("GET", "/academic/api/subjects/{subjectId}", "academic", "api/subjects/{subjectId}", "Academic Get Subject", "Academic Service (Proxy)"),
    ("POST", "/academic/api/subjects", "academic", "api/subjects", "Academic Create Subject", "Academic Service (Proxy)"),
    ("PUT", "/academic/api/subjects/{subjectId}", "academic", "api/subjects/{subjectId}", "Academic Update Subject", "Academic Service (Proxy)"),
    ("DELETE", "/academic/api/subjects/{subjectId}", "academic", "api/subjects/{subjectId}", "Academic Delete Subject", "Academic Service (Proxy)"),
    ("GET", "/academic/api/enrollments", "academic", "api/enrollments", "Academic List Enrollments", "Academic Service (Proxy)"),
    ("GET", "/academic/api/enrollments/student/{studentId}", "academic", "api/enrollments/student/{studentId}", "Academic Student Enrollment", "Academic Service (Proxy)"),
    ("POST", "/academic/api/enrollments", "academic", "api/enrollments", "Academic Enroll Student", "Academic Service (Proxy)"),
    ("PATCH", "/academic/api/enrollments/{enrollmentId}/transfer", "academic", "api/enrollments/{enrollmentId}/transfer", "Academic Transfer Student", "Academic Service (Proxy)"),
    ("POST", "/academic/api/enrollments/promote", "academic", "api/enrollments/promote", "Academic Promote Students", "Academic Service (Proxy)"),
    ("GET", "/academic/api/teacher-assignments", "academic", "api/teacher-assignments", "Academic List Teacher Assignments", "Academic Service (Proxy)"),
    ("GET", "/academic/api/teacher-assignments/teaching-load/{teacherId}", "academic", "api/teacher-assignments/teaching-load/{teacherId}", "Academic Teacher Load", "Academic Service (Proxy)"),
    ("POST", "/academic/api/teacher-assignments", "academic", "api/teacher-assignments", "Academic Create Teacher Assignment", "Academic Service (Proxy)"),
    ("DELETE", "/academic/api/teacher-assignments/{assignmentId}", "academic", "api/teacher-assignments/{assignmentId}", "Academic Delete Teacher Assignment", "Academic Service (Proxy)"),
    ("GET", "/academic/api/timetable", "academic", "api/timetable", "Academic Get Timetable", "Academic Service (Proxy)"),
    ("POST", "/academic/api/timetable", "academic", "api/timetable", "Academic Create Timetable Slot", "Academic Service (Proxy)"),
    ("POST", "/academic/api/timetable/bulk", "academic", "api/timetable/bulk", "Academic Create Timetable Slots Bulk", "Academic Service (Proxy)"),
    ("PUT", "/academic/api/timetable/{slotId}", "academic", "api/timetable/{slotId}", "Academic Update Timetable Slot", "Academic Service (Proxy)"),
    ("DELETE", "/academic/api/timetable/{slotId}", "academic", "api/timetable/{slotId}", "Academic Delete Timetable Slot", "Academic Service (Proxy)"),
    ("POST", "/academic/api/timetable/publish", "academic", "api/timetable/publish", "Academic Publish Timetable", "Academic Service (Proxy)"),
    # Homework & Assessment
    ("GET", "/assessment/health", "assessment", "health", "Assessment Health", "Assessment Service (Proxy)"),
    ("POST", "/assessment/api/v1/assignments", "assessment", "api/v1/assignments", "Assessment Create Assignment", "Assessment Service (Proxy)"),
    ("GET", "/assessment/api/v1/assignments", "assessment", "api/v1/assignments", "Assessment List Assignments", "Assessment Service (Proxy)"),
    ("GET", "/assessment/api/v1/assignments/{assignmentId}", "assessment", "api/v1/assignments/{assignmentId}", "Assessment Get Assignment", "Assessment Service (Proxy)"),
    ("PATCH", "/assessment/api/v1/assignments/{assignmentId}", "assessment", "api/v1/assignments/{assignmentId}", "Assessment Update Assignment", "Assessment Service (Proxy)"),
    ("POST", "/assessment/api/v1/assignments/{assignmentId}/publish", "assessment", "api/v1/assignments/{assignmentId}/publish", "Assessment Publish Assignment", "Assessment Service (Proxy)"),
    ("POST", "/assessment/api/v1/submissions", "assessment", "api/v1/submissions", "Assessment Submit Assignment", "Assessment Service (Proxy)"),
    ("GET", "/assessment/api/v1/submissions/assignment/{assignmentId}", "assessment", "api/v1/submissions/assignment/{assignmentId}", "Assessment List Assignment Submissions", "Assessment Service (Proxy)"),
    ("GET", "/assessment/api/v1/submissions/student/{studentId}", "assessment", "api/v1/submissions/student/{studentId}", "Assessment List Student Submissions", "Assessment Service (Proxy)"),
    ("POST", "/assessment/api/v1/grading/submissions/{submissionId}", "assessment", "api/v1/grading/submissions/{submissionId}", "Assessment Grade Submission", "Assessment Service (Proxy)"),
    ("GET", "/assessment/api/v1/grading/classes/{classId}/gradebook", "assessment", "api/v1/grading/classes/{classId}/gradebook", "Assessment Gradebook", "Assessment Service (Proxy)"),
    ("POST", "/assessment/api/v1/results/{submissionId}/publish", "assessment", "api/v1/results/{submissionId}/publish", "Assessment Publish Result", "Assessment Service (Proxy)"),
    ("GET", "/assessment/api/v1/results/student/{studentId}", "assessment", "api/v1/results/student/{studentId}", "Assessment Student Results", "Assessment Service (Proxy)"),
    # Learning Materials
    ("GET", "/materials/health", "materials", "health", "Materials Health", "Learning Materials Service (Proxy)"),
    ("GET", "/materials/ready", "materials", "ready", "Materials Readiness", "Learning Materials Service (Proxy)"),
    ("GET", "/materials/api/v1/materials", "materials", "api/v1/materials", "Materials List", "Learning Materials Service (Proxy)"),
    ("POST", "/materials/api/v1/materials", "materials", "api/v1/materials", "Materials Create", "Learning Materials Service (Proxy)"),
    ("GET", "/materials/api/v1/materials/search", "materials", "api/v1/materials/search", "Materials Search", "Learning Materials Service (Proxy)"),
    ("GET", "/materials/api/v1/materials/{materialId}/versions", "materials", "api/v1/materials/{materialId}/versions", "Materials Versions", "Learning Materials Service (Proxy)"),
    ("GET", "/materials/api/v1/materials/{materialId}/visibility", "materials", "api/v1/materials/{materialId}/visibility", "Materials Visibility", "Learning Materials Service (Proxy)"),
    # Communication
    ("GET", "/communication/health", "communication", "health", "Communication Health", "Communication Service (Proxy)"),
    ("POST", "/communication/api/v1/notices", "communication", "api/v1/notices", "Communication Create Notice", "Communication Service (Proxy)"),
    ("GET", "/communication/api/v1/notices", "communication", "api/v1/notices", "Communication List Notices", "Communication Service (Proxy)"),
    ("POST", "/communication/api/v1/messages", "communication", "api/v1/messages", "Communication Send Message", "Communication Service (Proxy)"),
    ("GET", "/communication/api/v1/conversations/{conversationId}/messages", "communication", "api/v1/conversations/{conversationId}/messages", "Communication Get Conversation Messages", "Communication Service (Proxy)"),
    ("POST", "/communication/api/v1/alerts", "communication", "api/v1/alerts", "Communication Create Alert", "Communication Service (Proxy)"),
    ("GET", "/communication/api/v1/users/{userId}/alerts", "communication", "api/v1/users/{userId}/alerts", "Communication Get User Alerts", "Communication Service (Proxy)"),
    ("POST", "/communication/api/v1/support-cases", "communication", "api/v1/support-cases", "Communication Create Support Case", "Communication Service (Proxy)"),
    # Monitoring
    ("GET", "/monitoring/health", "monitoring", "health", "Monitoring Health", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/dashboards/principal", "monitoring", "api/v1/dashboards/principal", "Monitoring Principal Dashboard", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/dashboards/sectional-head", "monitoring", "api/v1/dashboards/sectional-head", "Monitoring Sectional Head Dashboard", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/reports/assignment-completion", "monitoring", "api/v1/reports/assignment-completion", "Monitoring Assignment Completion Report", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/reports/academic-risk", "monitoring", "api/v1/reports/academic-risk", "Monitoring Academic Risk Report", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/reports/material-usage", "monitoring", "api/v1/reports/material-usage", "Monitoring Material Usage Report", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/kpis", "monitoring", "api/v1/kpis", "Monitoring KPIs", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/interventions", "monitoring", "api/v1/interventions", "Monitoring Interventions", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/risk-rules", "monitoring", "api/v1/risk-rules", "Monitoring Risk Rules", "Monitoring Service (Proxy)"),
    ("GET", "/monitoring/api/v1/audit-views/user-activity", "monitoring", "api/v1/audit-views/user-activity", "Monitoring User Activity Audit", "Monitoring Service (Proxy)"),
]


for method, gateway_path, service_key, upstream_template, summary, tag in DOCUMENTED_PROXY_ROUTES:
    router.add_api_route(
        gateway_path,
        _proxy_handler_factory(service_key, upstream_template),
        methods=[method],
        summary=summary,
        tags=[tag],
    )


@router.api_route("/identity", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/identity/{path:path}", methods=HTTP_METHODS, include_in_schema=False)
async def proxy_identity(request: Request, path: str = ""):
    return await proxy_to_service(request, "identity", path)


@router.api_route("/assessment", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/assessment/{path:path}", methods=HTTP_METHODS, include_in_schema=False)
async def proxy_assessment(request: Request, path: str = ""):
    return await proxy_to_service(request, "assessment", path)


@router.api_route("/materials", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/materials/{path:path}", methods=HTTP_METHODS, include_in_schema=False)
async def proxy_materials(request: Request, path: str = ""):
    return await proxy_to_service(request, "materials", path)


@router.api_route("/monitoring", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/monitoring/{path:path}", methods=HTTP_METHODS, include_in_schema=False)
async def proxy_monitoring(request: Request, path: str = ""):
    return await proxy_to_service(request, "monitoring", path)


@router.api_route("/academic", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/academic/{path:path}", methods=HTTP_METHODS, include_in_schema=False)
async def proxy_academic(request: Request, path: str = ""):
    return await proxy_to_service(request, "academic", path)


@router.api_route("/groups", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/groups/{path:path}", methods=HTTP_METHODS, include_in_schema=False)
async def proxy_groups(request: Request, path: str = ""):
    return await proxy_to_service(request, "groups", path)


@router.api_route("/communication", methods=HTTP_METHODS, include_in_schema=False)
@router.api_route("/communication/{path:path}", methods=HTTP_METHODS, include_in_schema=False)
async def proxy_communication(request: Request, path: str = ""):
    return await proxy_to_service(request, "communication", path)
