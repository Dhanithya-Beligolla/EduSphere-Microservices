"""
group_models/group_model.py
MongoDB document model for Group entity.
A group is a set of students within a class, optionally spanning a grade or house/club.
"""

from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import uuid


class GroupScope(str, Enum):
    CLASS = "CLASS"       # Within a single class
    GRADE = "GRADE"       # Across a whole grade
    HOUSE = "HOUSE"       # School house team
    CLUB = "CLUB"         # Co-curricular club


class GroupStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class GroupDocument(Document):
    groupId: str = Field(default_factory=lambda: f"GRP-{uuid.uuid4().hex[:6].upper()}")
    name: str
    classId: Optional[str] = None       # CLS-G09-A
    gradeId: Optional[str] = None       # G09
    schoolId: str
    academicYearId: str
    scope: GroupScope = GroupScope.CLASS
    status: GroupStatus = GroupStatus.ACTIVE
    createdBy: str                       # teacherId
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "groups"
        indexes = [
            "groupId",
            "classId",
            "schoolId",
            "academicYearId",
        ]


# ── Pydantic request/response schemas ──────────────────────────────────────

class GroupCreateRequest(BaseModel):
    name: str
    classId: Optional[str] = None
    gradeId: Optional[str] = None
    schoolId: str
    academicYearId: str
    scope: GroupScope = GroupScope.CLASS


class GroupResponse(BaseModel):
    groupId: str
    name: str
    classId: Optional[str]
    gradeId: Optional[str]
    schoolId: str
    academicYearId: str
    scope: GroupScope
    status: GroupStatus
    createdBy: str
    createdAt: datetime
