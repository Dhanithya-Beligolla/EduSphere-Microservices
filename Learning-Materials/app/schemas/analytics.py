"""
Analytics stub schemas.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class AnalyticsResponse(BaseModel):
    """Stub analytics data contract for a material."""
    material_id: str = Field(..., alias="materialId")
    view_count: int = Field(default=0, alias="viewCount")
    download_count: int = Field(default=0, alias="downloadCount")
    unique_viewers: int = Field(default=0, alias="uniqueViewers")
    last_accessed_at: datetime | None = Field(default=None, alias="lastAccessedAt")

    model_config = {"populate_by_name": True}
