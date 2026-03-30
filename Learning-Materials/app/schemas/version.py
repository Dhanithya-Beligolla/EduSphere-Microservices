"""
Material version schemas.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class CreateVersionRequest(BaseModel):
    """Request to add a new version to a material."""
    file_id: str | None = Field(default=None, alias="fileId")
    external_url: str | None = Field(default=None, alias="externalUrl")
    change_log: str = Field(default="", alias="changeLog", max_length=2000)

    model_config = {"populate_by_name": True}


class VersionResponse(BaseModel):
    """Version representation returned by the API."""
    id: str
    material_id: str = Field(..., alias="materialId")
    version_number: int = Field(..., alias="versionNumber")
    file_id: str | None = Field(default=None, alias="fileId")
    external_url: str | None = Field(default=None, alias="externalUrl")
    change_log: str = Field(default="", alias="changeLog")
    created_at: datetime | None = Field(default=None, alias="createdAt")
    created_by: str | None = Field(default=None, alias="createdBy")

    model_config = {"populate_by_name": True, "from_attributes": True}
