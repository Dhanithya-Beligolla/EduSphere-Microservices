from fastapi import HTTPException, status
from app.core.config import settings


async def validate_teacher_assignment(teacher_id: str, class_id: str, subject_id: str) -> bool:
    if not settings.academic_validation_enabled:
        return True

    # Replace with actual Academic Service call later.
    # For MVP, validation is configurable and mocked.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Academic service validation not implemented yet",
    )


async def validate_student_enrollment(student_id: str, class_id: str) -> bool:
    if not settings.academic_validation_enabled:
        return True

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Academic service validation not implemented yet",
    )