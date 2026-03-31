"""
group_models/peer_eval_model.py
MongoDB document model for PeerEvaluation.
Each student rates their fellow group members.
Only collected when peerEvaluationEnabled=True on the activity.
"""

from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import uuid


class PeerEvaluationDocument(Document):
    evaluationId: str = Field(default_factory=lambda: f"PEER-{uuid.uuid4().hex[:6].upper()}")
    activityId: str
    groupId: str
    evaluatorStudentId: str    # Student giving the score
    evaluateeStudentId: str    # Student receiving the score
    score: float = Field(..., ge=0, le=10)   # 0-10 scale
    comment: Optional[str] = None
    submittedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "peer_evaluations"
        indexes = [
            "evaluationId",
            "activityId",
            "groupId",
            "evaluatorStudentId",
            "evaluateeStudentId",
        ]


# ── Schemas ─────────────────────────────────────────────────────────────────

class PeerEvaluationCreateRequest(BaseModel):
    activityId: str
    groupId: str
    evaluateeStudentId: str
    score: float = Field(..., ge=0, le=10)
    comment: Optional[str] = None


class PeerEvaluationResponse(BaseModel):
    evaluationId: str
    activityId: str
    groupId: str
    evaluatorStudentId: str
    evaluateeStudentId: str
    score: float
    comment: Optional[str]
    submittedAt: datetime
