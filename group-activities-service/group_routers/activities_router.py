"""
group_routers/activities_router.py
Feature 2 — Group Activity Management
Endpoints:
  POST  /api/v1/group-activities                              → Create group activity
  POST  /api/v1/group-activities/{activityId}/assign-groups  → Attach groups to activity
  GET   /api/v1/group-activities/{activityId}                → Get activity details
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timezone

from group_models.activity_model import (
    GroupActivityDocument,
    GroupActivityCreateRequest,
    AssignGroupsRequest,
    GroupActivityResponse,
    ActivityStatus,
    GroupMode,
)
from group_models.group_model import GroupDocument, GroupCreateRequest, GroupScope, GroupStatus
from group_models.membership_model import GroupMembershipDocument, MemberRole
from group_core.responses import StandardResponse
from group_core.events import publish_event, GroupEvent
from group_core.security import get_current_user, require_role, UserContext

router = APIRouter(prefix="/api/v1", tags=["Group Activity Management"])


# ── POST /api/v1/group-activities ────────────────────────────────────────────
@router.post(
    "/group-activities",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a group activity",
    description=(
        "Subject teacher creates an activity. "
        "If groupMode=AUTO, groups are created automatically from enrolled students."
    ),
)
async def create_group_activity(
    payload: GroupActivityCreateRequest,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL")
    ),
):
    activity = GroupActivityDocument(
        **payload.model_dump(),
        createdBy=current_user.userId,
    )
    await activity.insert()

    # Auto-group creation handled at assign-groups step or separately
    return StandardResponse.success(
        {
            "activityId": activity.activityId,
            "status": activity.status,
            "groupMode": activity.groupMode,
        }
    )


# ── POST /api/v1/group-activities/{activityId}/assign-groups ─────────────────
@router.post(
    "/group-activities/{activityId}/assign-groups",
    response_model=StandardResponse,
    summary="Attach groups to an activity",
    description=(
        "Attach one or more existing groups to a published activity. "
        "Publishes group.activity.published event."
    ),
)
async def assign_groups_to_activity(
    activityId: str,
    payload: AssignGroupsRequest,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL")
    ),
):
    activity = await GroupActivityDocument.find_one(
        GroupActivityDocument.activityId == activityId
    )
    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity '{activityId}' not found.")

    # Validate group IDs exist
    for gid in payload.groupIds:
        grp = await GroupDocument.find_one(GroupDocument.groupId == gid)
        if not grp:
            raise HTTPException(status_code=404, detail=f"Group '{gid}' not found.")

    # Merge without duplicates
    existing = set(activity.assignedGroupIds)
    new_ids = set(payload.groupIds)
    activity.assignedGroupIds = list(existing | new_ids)
    activity.status = ActivityStatus.PUBLISHED
    activity.publishedAt = datetime.now(timezone.utc)
    activity.updatedAt = datetime.now(timezone.utc)
    await activity.save()

    await publish_event(
        GroupEvent.ACTIVITY_PUBLISHED,
        {
            "activityId": activity.activityId,
            "classId": activity.classId,
            "groupsAssigned": len(activity.assignedGroupIds),
        },
    )

    return StandardResponse.success(
        {
            "activityId": activity.activityId,
            "groupsCreated": len(activity.assignedGroupIds),
            "status": activity.status,
        }
    )


# ── GET /api/v1/group-activities/{activityId} ────────────────────────────────
@router.get(
    "/group-activities/{activityId}",
    response_model=StandardResponse,
    summary="Get activity details",
    description="Fetch full details of a group activity including assigned groups.",
)
async def get_activity_details(
    activityId: str,
    current_user: UserContext = Depends(get_current_user),
):
    activity = await GroupActivityDocument.find_one(
        GroupActivityDocument.activityId == activityId
    )
    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity '{activityId}' not found.")

    return StandardResponse.success(
        GroupActivityResponse(
            activityId=activity.activityId,
            activityTitle=activity.activityTitle,
            description=activity.description,
            classId=activity.classId,
            subjectId=activity.subjectId,
            groupMode=activity.groupMode,
            peerEvaluationEnabled=activity.peerEvaluationEnabled,
            markSplit=activity.markSplit,
            maxMarks=activity.maxMarks,
            dueAt=activity.dueAt,
            status=activity.status,
            assignedGroupIds=activity.assignedGroupIds,
            createdBy=activity.createdBy,
            createdAt=activity.createdAt,
        ).model_dump()
    )
