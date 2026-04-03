"""
group_routers/submissions_router.py
Feature 3 — Group Submission Management
Endpoints:
  POST  /api/v1/group-submissions   → Submit group work
  GET   /api/v1/group-submissions/{activityId}  → View all submissions for an activity
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from datetime import datetime, timezone

from group_models.submission_model import (
    GroupSubmissionDocument,
    GroupSubmissionCreateRequest,
    GroupSubmissionResponse,
    SubmissionStatus,
)
from group_models.activity_model import GroupActivityDocument, ActivityStatus
from group_core.responses import StandardResponse
from group_core.events import publish_event, GroupEvent
from group_core.security import get_current_user, require_role, UserContext

router = APIRouter(prefix="/api/v1", tags=["Group Submissions"])


# ── POST /api/v1/group-submissions ───────────────────────────────────────────
@router.post(
    "/group-submissions",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit group work",
    description=(
        "Any active group member can submit the group's work for an activity. "
        "Late submissions are flagged automatically based on the activity due date. "
        "Publishes group.submission.created event."
    ),
)
async def submit_group_work(
    payload: GroupSubmissionCreateRequest,
    current_user: UserContext = Depends(
        require_role("STUDENT", "CLASS_TEACHER", "SUBJECT_TEACHER")
    ),
):
    # Validate activity exists and is published
    activity = await GroupActivityDocument.find_one(
        GroupActivityDocument.activityId == payload.activityId
    )
    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity '{payload.activityId}' not found.")
    if activity.status != ActivityStatus.PUBLISHED:
        raise HTTPException(
            status_code=409,
            detail="Cannot submit to an activity that is not yet published.",
        )

    # Prevent duplicate submission for same group + activity
    existing = await GroupSubmissionDocument.find_one(
        GroupSubmissionDocument.activityId == payload.activityId,
        GroupSubmissionDocument.groupId == payload.groupId,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Group '{payload.groupId}' has already submitted for this activity.",
        )

    # Check if late
    now = datetime.now(timezone.utc)
    is_late = bool(activity.dueAt and now > activity.dueAt)

    submission = GroupSubmissionDocument(
        **payload.model_dump(),
        submittedBy=current_user.userId,
        isLate=is_late,
        status=SubmissionStatus.LATE if is_late else SubmissionStatus.SUBMITTED,
    )
    await submission.insert()

    await publish_event(
        GroupEvent.SUBMISSION_CREATED,
        {
            "submissionId": submission.submissionId,
            "activityId": submission.activityId,
            "groupId": submission.groupId,
            "isLate": is_late,
        },
    )

    return StandardResponse.success(
        GroupSubmissionResponse(
            submissionId=submission.submissionId,
            activityId=submission.activityId,
            groupId=submission.groupId,
            classId=submission.classId,
            submittedBy=submission.submittedBy,
            textContent=submission.textContent,
            attachments=submission.attachments,
            status=submission.status,
            isLate=submission.isLate,
            submittedAt=submission.submittedAt,
        ).model_dump()
    )


# ── GET /api/v1/group-submissions/{activityId} ───────────────────────────────
@router.get(
    "/group-submissions/{activityId}",
    response_model=StandardResponse,
    summary="View all submissions for an activity",
    description="Teacher views all group submissions for a specific activity.",
)
async def get_submissions_for_activity(
    activityId: str,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL", "SECTIONAL_HEAD")
    ),
):
    submissions = await GroupSubmissionDocument.find(
        GroupSubmissionDocument.activityId == activityId
    ).to_list()

    result = [
        GroupSubmissionResponse(
            submissionId=s.submissionId,
            activityId=s.activityId,
            groupId=s.groupId,
            classId=s.classId,
            submittedBy=s.submittedBy,
            textContent=s.textContent,
            attachments=s.attachments,
            status=s.status,
            isLate=s.isLate,
            submittedAt=s.submittedAt,
        ).model_dump()
        for s in submissions
    ]
    return StandardResponse.success(result)
