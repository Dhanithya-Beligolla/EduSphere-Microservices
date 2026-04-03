"""
Visibility schemas for material audience targeting.
"""

from pydantic import BaseModel, Field
from app.core.constants import VisibilityScopeType


class VisibilityConfig(BaseModel):
    """Visibility scope configuration for a learning material."""
    scope_type: VisibilityScopeType = Field(
        default=VisibilityScopeType.SCHOOL,
        alias="scopeType",
    )
    school_id: str | None = Field(default=None, alias="schoolId")
    section_ids: list[str] = Field(default_factory=list, alias="sectionIds")
    stream_ids: list[str] = Field(default_factory=list, alias="streamIds")
    grade_ids: list[str] = Field(default_factory=list, alias="gradeIds")
    class_ids: list[str] = Field(default_factory=list, alias="classIds")
    subject_ids: list[str] = Field(default_factory=list, alias="subjectIds")

    model_config = {"populate_by_name": True}


class UpdateVisibilityRequest(BaseModel):
    """Request body for updating material visibility."""
    scope_type: VisibilityScopeType | None = Field(default=None, alias="scopeType")
    section_ids: list[str] | None = Field(default=None, alias="sectionIds")
    stream_ids: list[str] | None = Field(default=None, alias="streamIds")
    grade_ids: list[str] | None = Field(default=None, alias="gradeIds")
    class_ids: list[str] | None = Field(default=None, alias="classIds")
    subject_ids: list[str] | None = Field(default=None, alias="subjectIds")

    model_config = {"populate_by_name": True}
