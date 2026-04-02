"""
group_routers/results_router.py
Feature 5 — Results & Analytics
Endpoints:
  POST  /api/v1/group-results/{activityId}/grade          → Grade a group activity (teacher)
  GET   /api/v1/students/{studentId}/group-activities     → Student group activity feed
  GET   /api/v1/classes/{classId}/group-performance       → Teacher analytics for a class
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from datetime import datetime, timezone
from collections import defaultdict

from group_models.result_model import (
    GroupResultDocument,
    GradeActivityRequest,
    GroupResultResponse,
    ResultStatus,
    IndividualScore,
)
from group_models.activity_model import GroupActivityDocument, ActivityStatus
from group_models.submission_model import GroupSubmissionDocument
from group_models.peer_eval_model import PeerEvaluationDocument
from group_models.membership_model import GroupMembershipDocument
from group_core.responses import StandardResponse
from group_core.events import publish_event, GroupEvent
from group_core.security import get_current_user, require_role, UserContext

router = APIRouter(prefix="/api/v1", tags=["Results & Analytics"])


# ── POST /api/v1/group-results/{activityId}/grade ────────────────────────────
@router.post(
    "/group-results/{activityId}/grade",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Grade a group activity",
    description=(
        "Teacher assigns a raw group score. "
        "Individual scores are computed from the markSplit on the activity "
        "combined with peer evaluation averages if peerEvaluationEnabled. "
        "Publishes group.result.published event."
    ),
)
async def grade_group_activity(
    activityId: str,
    payload: GradeActivityRequest,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL")
    ),
):
    activity = await GroupActivityDocument.find_one(
        GroupActivityDocument.activityId == activityId
    )
    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity '{activityId}' not found.")

    # Prevent duplicate grading for same group
    existing = await GroupResultDocument.find_one(
        GroupResultDocument.activityId == activityId,
        GroupResultDocument.groupId == payload.groupId,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Group '{payload.groupId}' has already been graded for this activity.",
        )

    mark_split = activity.markSplit
    group_weight = mark_split.groupScorePercent / 100
    individual_weight = mark_split.individualScorePercent / 100

    # Calculate individual scores
    individual_scores: list[IndividualScore] = []

    if payload.individualScores:
        # Teacher explicitly provided individual scores (moderation case)
        individual_scores = payload.individualScores
    else:
        # Auto-compute from group score + peer evaluations
        members = await GroupMembershipDocument.find(
            GroupMembershipDocument.groupId == payload.groupId,
            GroupMembershipDocument.status == "ACTIVE",
        ).to_list()

        group_portion = (payload.groupRawScore / payload.maxMarks) * 100 * group_weight

        for member in members:
            peer_scores_docs = await PeerEvaluationDocument.find(
                PeerEvaluationDocument.activityId == activityId,
                PeerEvaluationDocument.evaluateeStudentId == member.studentId,
            ).to_list()

            peer_avg = None
            if peer_scores_docs:
                peer_avg = sum(p.score for p in peer_scores_docs) / len(peer_scores_docs)
                # peer score is out of 10; scale to percentage
                individual_portion = (peer_avg / 10) * 100 * individual_weight
            else:
                # No peer scores: individual portion mirrors group score
                individual_portion = (payload.groupRawScore / payload.maxMarks) * 100 * individual_weight

            final_score = round((group_portion + individual_portion) * payload.maxMarks / 100, 2)

            individual_scores.append(
                IndividualScore(
                    studentId=member.studentId,
                    groupScore=round(group_portion * payload.maxMarks / 100, 2),
                    peerScore=round(peer_avg, 2) if peer_avg is not None else None,
                    individualScore=final_score,
                )
            )

    result = GroupResultDocument(
        activityId=activityId,
        groupId=payload.groupId,
        classId=payload.classId,
        schoolId=payload.schoolId,
        groupRawScore=payload.groupRawScore,
        maxMarks=payload.maxMarks,
        gradedBy=current_user.userId,
        feedback=payload.feedback,
        individualScores=individual_scores,
        status=ResultStatus.PUBLISHED,
        publishedAt=datetime.now(timezone.utc),
    )
    await result.insert()

    await publish_event(
        GroupEvent.RESULT_PUBLISHED,
        {
            "resultId": result.resultId,
            "activityId": activityId,
            "groupId": payload.groupId,
            "classId": payload.classId,
            "groupRawScore": payload.groupRawScore,
        },
    )

    return StandardResponse.success(
        GroupResultResponse(
            resultId=result.resultId,
            activityId=result.activityId,
            groupId=result.groupId,
            classId=result.classId,
            groupRawScore=result.groupRawScore,
            maxMarks=result.maxMarks,
            gradedBy=result.gradedBy,
            feedback=result.feedback,
            individualScores=result.individualScores,
            status=result.status,
            gradedAt=result.gradedAt,
            publishedAt=result.publishedAt,
        ).model_dump()
    )


# ── GET /api/v1/students/{studentId}/group-activities ────────────────────────
@router.get(
    "/students/{studentId}/group-activities",
    response_model=StandardResponse,
    summary="Student group activity feed",
    description=(
        "Returns all group activities a student is involved in, "
        "along with their group membership and result if graded."
    ),
)
async def get_student_group_activities(
    studentId: str,
    current_user: UserContext = Depends(get_current_user),
):
    # Role scoping: student can only see their own feed
    if current_user.role == "STUDENT" and current_user.userId != studentId:
        raise HTTPException(status_code=403, detail="You can only view your own group activities.")

    # Find all groups the student belongs to
    memberships = await GroupMembershipDocument.find(
        GroupMembershipDocument.studentId == studentId,
        GroupMembershipDocument.status == "ACTIVE",
    ).to_list()

    group_ids = [m.groupId for m in memberships]
    if not group_ids:
        return StandardResponse.success([])

    feed = []
    for membership in memberships:
        # Find activities assigned to this group
        activities = await GroupActivityDocument.find(
            GroupActivityDocument.assignedGroupIds == membership.groupId,
            GroupActivityDocument.status == ActivityStatus.PUBLISHED,
        ).to_list()

        for activity in activities:
            # Check if group has a result
            result = await GroupResultDocument.find_one(
                GroupResultDocument.activityId == activity.activityId,
                GroupResultDocument.groupId == membership.groupId,
            )

            individual_result = None
            if result:
                for ind in result.individualScores:
                    if ind.studentId == studentId:
                        individual_result = {
                            "groupScore": ind.groupScore,
                            "peerScore": ind.peerScore,
                            "individualScore": ind.individualScore,
                        }
                        break

            feed.append({
                "activityId": activity.activityId,
                "activityTitle": activity.activityTitle,
                "subjectId": activity.subjectId,
                "classId": activity.classId,
                "dueAt": activity.dueAt.isoformat() if activity.dueAt else None,
                "status": activity.status,
                "groupId": membership.groupId,
                "memberRole": membership.role,
                "peerEvaluationEnabled": activity.peerEvaluationEnabled,
                "result": individual_result,
            })

    return StandardResponse.success(feed)


# ── GET /api/v1/classes/{classId}/group-performance ──────────────────────────
@router.get(
    "/classes/{classId}/group-performance",
    response_model=StandardResponse,
    summary="Teacher analytics — class group performance",
    description=(
        "Returns an aggregated performance summary for all groups in a class: "
        "submission rate, average group score, peer evaluation completion, "
        "and per-activity breakdowns."
    ),
)
async def get_class_group_performance(
    classId: str,
    current_user: UserContext = Depends(
        require_role("SUBJECT_TEACHER", "CLASS_TEACHER", "PRINCIPAL", "SECTIONAL_HEAD", "DEPUTY")
    ),
):
    activities = await GroupActivityDocument.find(
        GroupActivityDocument.classId == classId
    ).to_list()

    if not activities:
        return StandardResponse.success({"classId": classId, "activities": []})

    activity_summaries = []
    for activity in activities:
        total_groups = len(activity.assignedGroupIds)

        submissions = await GroupSubmissionDocument.find(
            GroupSubmissionDocument.activityId == activity.activityId
        ).to_list()
        submitted_count = len(submissions)
        late_count = sum(1 for s in submissions if s.isLate)

        results = await GroupResultDocument.find(
            GroupResultDocument.activityId == activity.activityId
        ).to_list()
        graded_count = len(results)
        avg_score = (
            round(sum(r.groupRawScore for r in results) / len(results), 2)
            if results else None
        )

        peer_evals = await PeerEvaluationDocument.find(
            PeerEvaluationDocument.activityId == activity.activityId
        ).to_list()

        activity_summaries.append({
            "activityId": activity.activityId,
            "activityTitle": activity.activityTitle,
            "status": activity.status,
            "totalGroupsAssigned": total_groups,
            "submittedCount": submitted_count,
            "lateSubmissions": late_count,
            "submissionRate": round(submitted_count / total_groups * 100, 1) if total_groups else 0,
            "gradedCount": graded_count,
            "averageGroupScore": avg_score,
            "peerEvaluationsSubmitted": len(peer_evals),
            "peerEvaluationEnabled": activity.peerEvaluationEnabled,
        })

    return StandardResponse.success({
        "classId": classId,
        "totalActivities": len(activities),
        "activities": activity_summaries,
    })
