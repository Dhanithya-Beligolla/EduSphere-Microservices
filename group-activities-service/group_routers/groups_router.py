"""
group_routers/groups_router.py
Feature 1 — Group Management
Endpoints:
  POST   /api/v1/groups              → Create a group set
  GET    /api/v1/groups?classId=...  → List groups by class
  POST   /api/v1/groups/{groupId}/members       → Add a member to a group
  PATCH  /api/v1/group-memberships/{membershipId} → Change member role
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from datetime import datetime, timezone

from group_models.group_model import (
    GroupDocument,
    GroupCreateRequest,
    GroupResponse,
)
from group_models.membership_model import (
    GroupMembershipDocument,
    AddMemberRequest,
    UpdateMemberRoleRequest,
    MembershipResponse,
)
from group_core.responses import StandardResponse
from group_core.events import publish_event, GroupEvent
from group_core.security import get_current_user, require_role, UserContext

router = APIRouter(prefix="/api/v1", tags=["Group Management"])


# ── POST /api/v1/groups ──────────────────────────────────────────────────────
@router.post(
    "/groups",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a group set",
    description="Class teacher or subject teacher creates one or more groups for a class.",
)
async def create_group(
    payload: GroupCreateRequest,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL", "SECTIONAL_HEAD")
    ),
):
    group = GroupDocument(
        **payload.model_dump(),
        createdBy=current_user.userId,
    )
    await group.insert()

    await publish_event(
        GroupEvent.GROUP_CREATED,
        {"groupId": group.groupId, "classId": group.classId, "schoolId": group.schoolId},
    )

    return StandardResponse.success(
        GroupResponse(
            groupId=group.groupId,
            name=group.name,
            classId=group.classId,
            gradeId=group.gradeId,
            schoolId=group.schoolId,
            academicYearId=group.academicYearId,
            scope=group.scope,
            status=group.status,
            createdBy=group.createdBy,
            createdAt=group.createdAt,
        ).model_dump()
    )


# ── GET /api/v1/groups ───────────────────────────────────────────────────────
@router.get(
    "/groups",
    response_model=StandardResponse,
    summary="List groups",
    description="List all groups for a given class.",
)
async def list_groups(
    classId: str = Query(..., description="Class ID e.g. CLS-G09-A"),
    current_user: UserContext = Depends(get_current_user),
):
    groups = await GroupDocument.find(GroupDocument.classId == classId).to_list()
    result = [
        GroupResponse(
            groupId=g.groupId,
            name=g.name,
            classId=g.classId,
            gradeId=g.gradeId,
            schoolId=g.schoolId,
            academicYearId=g.academicYearId,
            scope=g.scope,
            status=g.status,
            createdBy=g.createdBy,
            createdAt=g.createdAt,
        ).model_dump()
        for g in groups
    ]
    return StandardResponse.success(result)


# ── POST /api/v1/groups/{groupId}/members ────────────────────────────────────
@router.post(
    "/groups/{groupId}/members",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a member to a group",
    description="Assign a student to a group with an optional role.",
)
async def add_member(
    groupId: str,
    payload: AddMemberRequest,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL", "SECTIONAL_HEAD")
    ),
):
    group = await GroupDocument.find_one(GroupDocument.groupId == groupId)
    if not group:
        raise HTTPException(status_code=404, detail=f"Group '{groupId}' not found.")

    # Prevent duplicate membership
    existing = await GroupMembershipDocument.find_one(
        GroupMembershipDocument.groupId == groupId,
        GroupMembershipDocument.studentId == payload.studentId,
        GroupMembershipDocument.status == "ACTIVE",
    )
    if existing:
        raise HTTPException(status_code=409, detail="Student is already a member of this group.")

    membership = GroupMembershipDocument(
        groupId=groupId,
        studentId=payload.studentId,
        role=payload.role,
        updatedBy=current_user.userId,
    )
    await membership.insert()

    return StandardResponse.success(
        MembershipResponse(
            membershipId=membership.membershipId,
            groupId=membership.groupId,
            studentId=membership.studentId,
            role=membership.role,
            status=membership.status,
            joinedAt=membership.joinedAt,
        ).model_dump()
    )


# ── PATCH /api/v1/group-memberships/{membershipId} ──────────────────────────
@router.patch(
    "/group-memberships/{membershipId}",
    response_model=StandardResponse,
    summary="Change member role",
    description="Update the role of a group member (e.g. promote to LEADER).",
)
async def update_member_role(
    membershipId: str,
    payload: UpdateMemberRoleRequest,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL", "SECTIONAL_HEAD")
    ),
):
    membership = await GroupMembershipDocument.find_one(
        GroupMembershipDocument.membershipId == membershipId
    )
    if not membership:
        raise HTTPException(status_code=404, detail=f"Membership '{membershipId}' not found.")

    membership.role = payload.role
    membership.updatedAt = datetime.now(timezone.utc)
    membership.updatedBy = current_user.userId
    await membership.save()

    return StandardResponse.success(
        MembershipResponse(
            membershipId=membership.membershipId,
            groupId=membership.groupId,
            studentId=membership.studentId,
            role=membership.role,
            status=membership.status,
            joinedAt=membership.joinedAt,
        ).model_dump()
    )
