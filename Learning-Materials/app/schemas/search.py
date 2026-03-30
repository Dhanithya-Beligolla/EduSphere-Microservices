"""
Search and filter parameter schemas.
"""

from pydantic import BaseModel, Field
from app.core.constants import ResourceType, Medium, MaterialStatus


class SearchParams(BaseModel):
    """Query parameters for searching and filtering materials."""
    q: str | None = Field(default=None, description="Free-text search query")
    grade_id: str | None = Field(default=None, alias="gradeId")
    subject_id: str | None = Field(default=None, alias="subjectId")
    term_id: str | None = Field(default=None, alias="termId")
    unit_id: str | None = Field(default=None, alias="unitId")
    medium: Medium | None = None
    resource_type: ResourceType | None = Field(default=None, alias="resourceType")
    status: MaterialStatus | None = None
    tags: str | None = Field(default=None, description="Comma-separated tags")
    date_from: str | None = Field(default=None, alias="dateFrom")
    date_to: str | None = Field(default=None, alias="dateTo")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100, alias="pageSize")
    sort_by: str = Field(default="createdAt", alias="sortBy")
    sort_order: str = Field(default="desc", alias="sortOrder", pattern="^(asc|desc)$")

    model_config = {"populate_by_name": True}
