from pydantic import BaseModel
from datetime import datetime


class PublishedResultOut(BaseModel):
    submission_id: int
    student_id: str
    assignment_id: int
    marks_obtained: float
    grade: str | None
    feedback_summary: str | None
    published_at: datetime | None