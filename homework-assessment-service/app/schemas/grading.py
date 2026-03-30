from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class GradeSubmissionRequest(BaseModel):
    marks_obtained: float = Field(ge=0)
    grade: str | None = None
    feedback_summary: str | None = None


class GradeEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submission_id: int
    marks_obtained: float
    grade: str | None
    feedback_summary: str | None
    graded_by: str
    graded_at: datetime
    is_published: bool
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime