"""
Material request/response schemas — Pydantic v2 models.
"""

from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from app.core.constants import ResourceType, Medium, MaterialStatus
from app.schemas.visibility import VisibilityConfig


class CreateMaterialRequest(BaseModel):
    """Request body for creating a new learning material."""
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=5000)
    subject_id: str | None = Field(default=None, alias="subjectId")
    grade_id: str | None = Field(default=None, alias="gradeId")
    term_id: str | None = Field(default=None, alias="termId")
    unit_id: str | None = Field(default=None, alias="unitId")
    medium: Medium | None = None
    resource_type: ResourceType = Field(..., alias="resourceType")
    tags: list[str] = Field(default_factory=list)
    visibility: VisibilityConfig | None = None
    file_id: str | None = Field(default=None, alias="fileId")
    external_url: str | None = Field(default=None, alias="externalUrl")
    thumbnail_url: str | None = Field(default=None, alias="thumbnailUrl")
    language: str | None = None

    model_config = {"populate_by_name": True}


class UpdateMaterialRequest(BaseModel):
    """Request body for partially updating a learning material."""
    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=5000)
    subject_id: str | None = Field(default=None, alias="subjectId")
    grade_id: str | None = Field(default=None, alias="gradeId")
    term_id: str | None = Field(default=None, alias="termId")
    unit_id: str | None = Field(default=None, alias="unitId")
    medium: Medium | None = None
    resource_type: ResourceType | None = Field(default=None, alias="resourceType")
    tags: list[str] | None = None
    file_id: str | None = Field(default=None, alias="fileId")
    external_url: str | None = Field(default=None, alias="externalUrl")
    thumbnail_url: str | None = Field(default=None, alias="thumbnailUrl")
    language: str | None = None

    model_config = {"populate_by_name": True}


class MaterialResponse(BaseModel):
    """Full material representation returned by the API."""
    id: str
    title: str
    description: str | None = None
    subject_id: str | None = Field(default=None, alias="subjectId")
    grade_id: str | None = Field(default=None, alias="gradeId")
    term_id: str | None = Field(default=None, alias="termId")
    unit_id: str | None = Field(default=None, alias="unitId")
    medium: str | None = None
    resource_type: str = Field(..., alias="resourceType")
    tags: list[str] = Field(default_factory=list)
    status: str
    visibility: VisibilityConfig | None = None
    current_version: int = Field(default=1, alias="currentVersion")
    file_id: str | None = Field(default=None, alias="fileId")
    external_url: str | None = Field(default=None, alias="externalUrl")
    thumbnail_url: str | None = Field(default=None, alias="thumbnailUrl")
    language: str | None = None
    school_id: str = Field(..., alias="schoolId")
    published_at: datetime | None = Field(default=None, alias="publishedAt")
    published_by: str | None = Field(default=None, alias="publishedBy")
    created_at: datetime | None = Field(default=None, alias="createdAt")
    created_by: str | None = Field(default=None, alias="createdBy")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    updated_by: str | None = Field(default=None, alias="updatedBy")
    archived_at: datetime | None = Field(default=None, alias="archivedAt")
    archived_by: str | None = Field(default=None, alias="archivedBy")

    model_config = {"populate_by_name": True, "from_attributes": True}
