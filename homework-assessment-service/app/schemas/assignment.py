from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.utils.enums import AssignmentType, AssignmentStatus, LanguageMedium


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    type: AssignmentType
    class_id: str
    subject_id: str
    publish_at: datetime | None = None
    due_at: datetime
    total_marks: float = Field(gt=0)
    allow_late_submission: bool = False
    max_attempts: int = Field(default=1, ge=1)
    language_medium: LanguageMedium | None = None


class AssignmentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    publish_at: datetime | None = None
    due_at: datetime | None = None
    total_marks: float | None = Field(default=None, gt=0)
    allow_late_submission: bool | None = None
    max_attempts: int | None = Field(default=None, ge=1)
    language_medium: LanguageMedium | None = None


class AssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    type: AssignmentType
    class_id: str
    subject_id: str
    teacher_id: str
    publish_at: datetime | None
    due_at: datetime
    total_marks: float
    allow_late_submission: bool
    max_attempts: int
    language_medium: LanguageMedium | None
    status: AssignmentStatus
    created_at: datetime
    updated_at: datetime