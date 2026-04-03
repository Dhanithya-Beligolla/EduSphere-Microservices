"""
group_models/submission_model.py
MongoDB document model for GroupSubmission.
One submission record per group per activity.
"""

from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import uuid


class SubmissionStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    LATE = "LATE"
    GRADED = "GRADED"
    RESUBMISSION_REQUIRED = "RESUBMISSION_REQUIRED"


class FileAttachment(BaseModel):
    fileId: str
    fileName: str
    fileUrl: Optional[str] = None


class GroupSubmissionDocument(Document):
    submissionId: str = Field(default_factory=lambda: f"GSUB-{uuid.uuid4().hex[:6].upper()}")
    activityId: str
    groupId: str
    classId: str
    schoolId: str
    submittedBy: str           # studentId who clicked submit
    textContent: Optional[str] = None
    attachments: list[FileAttachment] = []
    notes: Optional[str] = None
    status: SubmissionStatus = SubmissionStatus.SUBMITTED
    isLate: bool = False
    submittedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "group_submissions"
        indexes = [
            "submissionId",
            "activityId",
            "groupId",
            "schoolId",
        ]


# ── Schemas ─────────────────────────────────────────────────────────────────

class GroupSubmissionCreateRequest(BaseModel):
    activityId: str
    groupId: str
    classId: str
    schoolId: str
    textContent: Optional[str] = None
    attachments: list[FileAttachment] = []
    notes: Optional[str] = None


class GroupSubmissionResponse(BaseModel):
    submissionId: str
    activityId: str
    groupId: str
    classId: str
    submittedBy: str
    textContent: Optional[str]
    attachments: list[FileAttachment]
    status: SubmissionStatus
    isLate: bool
    submittedAt: datetime
