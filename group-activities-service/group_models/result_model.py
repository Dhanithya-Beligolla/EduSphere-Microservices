"""
group_models/result_model.py
MongoDB document model for GroupResult.
Stores the final teacher-assigned group score and computed individual scores.
"""

from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import uuid


class ResultStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class IndividualScore(BaseModel):
    studentId: str
    groupScore: float          # Weighted portion from group mark
    peerScore: Optional[float] = None   # Average peer evaluation score
    individualScore: float     # Final weighted individual mark
    comment: Optional[str] = None


class GroupResultDocument(Document):
    resultId: str = Field(default_factory=lambda: f"GRES-{uuid.uuid4().hex[:6].upper()}")
    activityId: str
    groupId: str
    classId: str
    schoolId: str
    groupRawScore: float          # Teacher's mark for the group as a whole
    maxMarks: float
    gradedBy: str                 # teacherId
    feedback: Optional[str] = None
    individualScores: list[IndividualScore] = []
    status: ResultStatus = ResultStatus.DRAFT
    gradedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    publishedAt: Optional[datetime] = None

    class Settings:
        name = "group_results"
        indexes = [
            "resultId",
            "activityId",
            "groupId",
            "classId",
            "schoolId",
            "status",
        ]


# ── Schemas ─────────────────────────────────────────────────────────────────

class GradeActivityRequest(BaseModel):
    groupId: str
    classId: str
    schoolId: str
    groupRawScore: float
    maxMarks: float
    feedback: Optional[str] = None
    individualScores: list[IndividualScore] = []


class GroupResultResponse(BaseModel):
    resultId: str
    activityId: str
    groupId: str
    classId: str
    groupRawScore: float
    maxMarks: float
    gradedBy: str
    feedback: Optional[str]
    individualScores: list[IndividualScore]
    status: ResultStatus
    gradedAt: datetime
    publishedAt: Optional[datetime]
