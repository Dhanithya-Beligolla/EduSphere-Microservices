import os
from datetime import datetime, timezone
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.services.academic_client import validate_student_enrollment
from app.utils.enums import AssignmentStatus, SubmissionStatus

async def create_submission(
    db: Session,
    assignment_id: int,
    student_id: str,
    submission_text: str | None,
    file: UploadFile | None,
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.status != AssignmentStatus.PUBLISHED.value:
        raise HTTPException(status_code=409, detail="Assignment is not published")

    await validate_student_enrollment(student_id, assignment.class_id)

    attempt_count = db.query(Submission).filter(
        Submission.assignment_id == assignment_id,
        Submission.student_id == student_id,
    ).count()

    if attempt_count >= assignment.max_attempts:
        raise HTTPException(status_code=409, detail="Maximum submission attempts reached")

    now = datetime.now(timezone.utc)
    due = assignment.due_at
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)

    is_late = now > due
    if is_late and not assignment.allow_late_submission:
        raise HTTPException(status_code=409, detail="Late submissions are not allowed")

    if not submission_text and not file:
        raise HTTPException(status_code=400, detail="Provide submission text or a file")

    file_url = None
    original_file_name = None

    if file:
        os.makedirs(settings.upload_dir, exist_ok=True)
        original_file_name = file.filename
        stored_name = f"{student_id}_{assignment_id}_{attempt_count + 1}_{file.filename}"
        full_path = os.path.join(settings.upload_dir, stored_name)

        content = await file.read()
        size_limit = settings.max_file_size_mb * 1024 * 1024
        if len(content) > size_limit:
            raise HTTPException(status_code=400, detail="Uploaded file exceeds size limit")

        with open(full_path, "wb") as f:
            f.write(content)

        file_url = full_path

    submission = Submission(
        assignment_id=assignment_id,
        student_id=student_id,
        submission_text=submission_text,
        file_url=file_url,
        original_file_name=original_file_name,
        is_late=is_late,
        attempt_no=attempt_count + 1,
        status=SubmissionStatus.RESUBMITTED.value if attempt_count > 0 else SubmissionStatus.SUBMITTED.value,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def list_assignment_submissions(db: Session, assignment_id: int, teacher_id: str):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.teacher_id != teacher_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return db.query(Submission).filter(Submission.assignment_id == assignment_id).order_by(Submission.submitted_at.desc()).all()


def list_student_submissions(db: Session, student_id: str, current_user_id: str, current_role: str):
    if current_role == "STUDENT" and student_id != current_user_id:
        raise HTTPException(status_code=403, detail="Students can only view their own submissions")

    return db.query(Submission).filter(Submission.student_id == student_id).order_by(Submission.submitted_at.desc()).all()


def get_submission(db: Session, submission_id: int):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission