"""
group_models/membership_model.py
MongoDB document model for GroupMembership.
Tracks which students belong to a group and their assigned roles.
"""

from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import uuid


class MemberRole(str, Enum):
    LEADER = "LEADER"
    SECRETARY = "SECRETARY"
    PRESENTER = "PRESENTER"
    RESEARCHER = "RESEARCHER"
    MEMBER = "MEMBER"


class MembershipStatus(str, Enum):
    ACTIVE = "ACTIVE"
    REMOVED = "REMOVED"


class GroupMembershipDocument(Document):
    membershipId: str = Field(default_factory=lambda: f"MEM-{uuid.uuid4().hex[:6].upper()}")
    groupId: str
    studentId: str
    role: MemberRole = MemberRole.MEMBER
    status: MembershipStatus = MembershipStatus.ACTIVE
    joinedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedBy: Optional[str] = None

    class Settings:
        name = "group_memberships"
        indexes = [
            "membershipId",
            "groupId",
            "studentId",
        ]


# ── Schemas ─────────────────────────────────────────────────────────────────

class AddMemberRequest(BaseModel):
    studentId: str
    role: MemberRole = MemberRole.MEMBER


class UpdateMemberRoleRequest(BaseModel):
    role: MemberRole


class MembershipResponse(BaseModel):
    membershipId: str
    groupId: str
    studentId: str
    role: MemberRole
    status: MembershipStatus
    joinedAt: datetime
