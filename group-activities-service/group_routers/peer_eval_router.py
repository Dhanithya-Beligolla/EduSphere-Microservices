"""
group_routers/peer_eval_router.py
Feature 4 — Peer Evaluation
Endpoints:
  POST  /api/v1/peer-evaluations              → Submit a peer score
  GET   /api/v1/peer-evaluations/{activityId} → Get all peer evaluations for an activity
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timezone

from group_models.peer_eval_model import (
    PeerEvaluationDocument,
    PeerEvaluationCreateRequest,
    PeerEvaluationResponse,
)
from group_models.activity_model import GroupActivityDocument
from group_models.membership_model import GroupMembershipDocument
from group_core.responses import StandardResponse
from group_core.events import publish_event, GroupEvent
from group_core.security import get_current_user, require_role, UserContext

router = APIRouter(prefix="/api/v1", tags=["Peer Evaluation"])


# ── POST /api/v1/peer-evaluations ────────────────────────────────────────────
@router.post(
    "/peer-evaluations",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a peer evaluation score",
    description=(
        "A student submits a score (0–10) for another member of their group. "
        "Only allowed when the activity has peerEvaluationEnabled=True. "
        "A student cannot evaluate themselves. "
        "Publishes group.peer-evaluation.submitted event."
    ),
)
async def submit_peer_evaluation(
    payload: PeerEvaluationCreateRequest,
    current_user: UserContext = Depends(require_role("STUDENT")),
):
    # Self-evaluation guard
    if current_user.userId == payload.evaluateeStudentId:
        raise HTTPException(status_code=400, detail="You cannot evaluate yourself.")

    # Activity must have peer evaluation enabled
    activity = await GroupActivityDocument.find_one(
        GroupActivityDocument.activityId == payload.activityId
    )
    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity '{payload.activityId}' not found.")
    if not activity.peerEvaluationEnabled:
        raise HTTPException(
            status_code=409, detail="Peer evaluation is not enabled for this activity."
        )

    # Evaluator must be in the group
    evaluator_membership = await GroupMembershipDocument.find_one(
        GroupMembershipDocument.groupId == payload.groupId,
        GroupMembershipDocument.studentId == current_user.userId,
        GroupMembershipDocument.status == "ACTIVE",
    )
    if not evaluator_membership:
        raise HTTPException(
            status_code=403, detail="You are not an active member of this group."
        )

    # Evaluatee must also be in the group
    evaluatee_membership = await GroupMembershipDocument.find_one(
        GroupMembershipDocument.groupId == payload.groupId,
        GroupMembershipDocument.studentId == payload.evaluateeStudentId,
        GroupMembershipDocument.status == "ACTIVE",
    )
    if not evaluatee_membership:
        raise HTTPException(
            status_code=404,
            detail=f"Student '{payload.evaluateeStudentId}' is not a member of this group.",
        )

    # Prevent duplicate evaluation (same evaluator → evaluatee for same activity)
    existing = await PeerEvaluationDocument.find_one(
        PeerEvaluationDocument.activityId == payload.activityId,
        PeerEvaluationDocument.evaluatorStudentId == current_user.userId,
        PeerEvaluationDocument.evaluateeStudentId == payload.evaluateeStudentId,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="You have already evaluated this student for this activity.",
        )

    evaluation = PeerEvaluationDocument(
        **payload.model_dump(),
        evaluatorStudentId=current_user.userId,
    )
    await evaluation.insert()

    await publish_event(
        GroupEvent.PEER_EVAL_SUBMITTED,
        {
            "evaluationId": evaluation.evaluationId,
            "activityId": evaluation.activityId,
            "groupId": evaluation.groupId,
            "evaluatorStudentId": evaluation.evaluatorStudentId,
            "evaluateeStudentId": evaluation.evaluateeStudentId,
        },
    )

    return StandardResponse.success(
        PeerEvaluationResponse(
            evaluationId=evaluation.evaluationId,
            activityId=evaluation.activityId,
            groupId=evaluation.groupId,
            evaluatorStudentId=evaluation.evaluatorStudentId,
            evaluateeStudentId=evaluation.evaluateeStudentId,
            score=evaluation.score,
            comment=evaluation.comment,
            submittedAt=evaluation.submittedAt,
        ).model_dump()
    )


# ── GET /api/v1/peer-evaluations/{activityId} ────────────────────────────────
@router.get(
    "/peer-evaluations/{activityId}",
    response_model=StandardResponse,
    summary="View all peer evaluations for an activity",
    description="Teacher or class teacher views all submitted peer scores for an activity.",
)
async def get_peer_evaluations(
    activityId: str,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL", "SECTIONAL_HEAD")
    ),
):
    evals = await PeerEvaluationDocument.find(
        PeerEvaluationDocument.activityId == activityId
    ).to_list()

    result = [
        PeerEvaluationResponse(
            evaluationId=e.evaluationId,
            activityId=e.activityId,
            groupId=e.groupId,
            evaluatorStudentId=e.evaluatorStudentId,
            evaluateeStudentId=e.evaluateeStudentId,
            score=e.score,
            comment=e.comment,
            submittedAt=e.submittedAt,
        ).model_dump()
        for e in evals
    ]
    return StandardResponse.success(result)
