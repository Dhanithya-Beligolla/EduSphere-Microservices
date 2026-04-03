"""
group_models/activity_model.py
MongoDB document model for GroupActivity.
A single activity (project, presentation, practical task) assigned to one or many groups.
"""

from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import uuid


class ActivityType(str, Enum):
    PROJECT = "PROJECT"
    PRESENTATION = "PRESENTATION"
    PRACTICAL = "PRACTICAL"
    CLUB_TASK = "CLUB_TASK"
    RESEARCH = "RESEARCH"


class GroupMode(str, Enum):
    AUTO = "AUTO"    # System creates groups automatically
    MANUAL = "MANUAL"  # Teacher assigns groups manually


class ActivityStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class MarkSplit(BaseModel):
    groupScorePercent: int = Field(70, ge=0, le=100)
    individualScorePercent: int = Field(30, ge=0, le=100)


class GroupActivityDocument(Document):
    activityId: str = Field(default_factory=lambda: f"GACT-{uuid.uuid4().hex[:6].upper()}")
    activityTitle: str
    description: Optional[str] = None
    classId: str
    subjectId: str
    schoolId: str
    academicYearId: str
    activityType: ActivityType = ActivityType.PROJECT
    groupMode: GroupMode = GroupMode.MANUAL
    groupSize: Optional[int] = None          # Used when groupMode=AUTO
    peerEvaluationEnabled: bool = False
    markSplit: MarkSplit = Field(default_factory=MarkSplit)
    maxMarks: int = 100
    dueAt: Optional[datetime] = None
    publishedAt: Optional[datetime] = None
    status: ActivityStatus = ActivityStatus.DRAFT
    assignedGroupIds: list[str] = []         # Populated after assign-groups
    createdBy: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "group_activities"
        indexes = [
            "activityId",
            "classId",
            "subjectId",
            "schoolId",
            "status",
        ]


# ── Schemas ─────────────────────────────────────────────────────────────────

class GroupActivityCreateRequest(BaseModel):
    activityTitle: str
    description: Optional[str] = None
    classId: str
    subjectId: str
    schoolId: str
    academicYearId: str
    activityType: ActivityType = ActivityType.PROJECT
    groupMode: GroupMode = GroupMode.MANUAL
    groupSize: Optional[int] = None
    peerEvaluationEnabled: bool = False
    markSplit: MarkSplit = Field(default_factory=MarkSplit)
    maxMarks: int = 100
    dueAt: Optional[datetime] = None


class AssignGroupsRequest(BaseModel):
    groupIds: list[str]


class GroupActivityResponse(BaseModel):
    activityId: str
    activityTitle: str
    description: Optional[str]
    classId: str
    subjectId: str
    groupMode: GroupMode
    peerEvaluationEnabled: bool
    markSplit: MarkSplit
    maxMarks: int
    dueAt: Optional[datetime]
    status: ActivityStatus
    assignedGroupIds: list[str]
    createdBy: str
    createdAt: datetime
