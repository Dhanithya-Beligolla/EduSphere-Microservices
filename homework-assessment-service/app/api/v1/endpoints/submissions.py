from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_roles
from app.schemas.common import StandardResponse
from app.schemas.submission import SubmissionOut
from app.services import submission_service

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post("", response_model=StandardResponse)
async def create_submission(
    assignment_id: int = Form(...),
    submission_text: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("STUDENT")),
):
    submission = await submission_service.create_submission(
        db=db,
        assignment_id=assignment_id,
        student_id=current_user["id"],
        submission_text=submission_text,
        file=file,
    )
    return StandardResponse(
        message="Submission created successfully",
        data=SubmissionOut.model_validate(submission),
    )


@router.get("/assignment/{assignment_id}", response_model=StandardResponse)
def list_assignment_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("SUBJECT_TEACHER", "CLASS_TEACHER")),
):
    submissions = submission_service.list_assignment_submissions(
        db, assignment_id, current_user["id"]
    )
    return StandardResponse(
        message="Assignment submissions fetched successfully",
        data=[SubmissionOut.model_validate(item) for item in submissions],
    )


@router.get("/student/{student_id}", response_model=StandardResponse)
def list_student_submissions(
    student_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    submissions = submission_service.list_student_submissions(
        db, student_id, current_user["id"], current_user["role"]
    )
    return StandardResponse(
        message="Student submissions fetched successfully",
        data=[SubmissionOut.model_validate(item) for item in submissions],
    )