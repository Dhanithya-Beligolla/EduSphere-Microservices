from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_roles
from app.schemas.common import StandardResponse
from app.schemas.grading import GradeSubmissionRequest, GradeEntryOut
from app.services import grading_service

router = APIRouter(prefix="/grading", tags=["Grading"])


@router.post("/submissions/{submission_id}", response_model=StandardResponse)
def grade_submission(
    submission_id: int,
    payload: GradeSubmissionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("SUBJECT_TEACHER", "CLASS_TEACHER")),
):
    grade = grading_service.grade_submission(
        db, submission_id, payload, current_user["id"]
    )
    return StandardResponse(
        message="Submission graded successfully",
        data=GradeEntryOut.model_validate(grade),
    )


@router.get("/classes/{class_id}/gradebook", response_model=StandardResponse)
def get_gradebook(
    class_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("CLASS_TEACHER", "ADMIN", "SUPER_ADMIN")),
):
    gradebook = grading_service.get_gradebook(db, class_id)
    return StandardResponse(
        message="Gradebook fetched successfully",
        data=gradebook,
    )