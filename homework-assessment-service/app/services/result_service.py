from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.models.grade_entry import GradeEntry



def publish_result(db: Session, submission_id: int, teacher_id: str):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if not submission.assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if submission.assignment.teacher_id != teacher_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    grade_entry = db.query(GradeEntry).filter(GradeEntry.submission_id == submission_id).first()
    if not grade_entry:
        raise HTTPException(status_code=409, detail="Submission has not been graded yet")

    grade_entry.is_published = True
    grade_entry.published_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(grade_entry)
    return grade_entry


def list_student_results(db: Session, student_id: str, current_user_id: str, current_role: str):
    if current_role == "STUDENT" and student_id != current_user_id:
        raise HTTPException(status_code=403, detail="Students can only view their own results")

    submissions = db.query(Submission).filter(Submission.student_id == student_id).all()
    published_results = []

    for submission in submissions:
        if submission.grade_entry and submission.grade_entry.is_published:
            published_results.append(
                {
                    "submission_id": submission.id,
                    "student_id": submission.student_id,
                    "assignment_id": submission.assignment_id,
                    "marks_obtained": submission.grade_entry.marks_obtained,
                    "grade": submission.grade_entry.grade,
                    "feedback_summary": submission.grade_entry.feedback_summary,
                    "published_at": submission.grade_entry.published_at,
                }
            )

    return published_results