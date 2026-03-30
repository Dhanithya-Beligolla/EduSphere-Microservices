from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assignment_id: int
    student_id: str
    submission_text: str | None
    file_url: str | None
    original_file_name: str | None
    submitted_at: datetime
    is_late: bool
    attempt_no: int
    status: str
    created_at: datetime
    updated_at: datetime