from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.models.grade_entry import GradeEntry
from app.schemas.grading import GradeSubmissionRequest
from app.utils.enums import SubmissionStatus



def grade_submission(db: Session, submission_id: int, payload: GradeSubmissionRequest, teacher_id: str):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.teacher_id != teacher_id:
        raise HTTPException(status_code=403, detail="Only the assignment teacher can grade this submission")

    if payload.marks_obtained > assignment.total_marks:
        raise HTTPException(status_code=400, detail="Marks cannot exceed assignment total marks")

    grade_entry = db.query(GradeEntry).filter(GradeEntry.submission_id == submission_id).first()
    if grade_entry:
        grade_entry.marks_obtained = payload.marks_obtained
        grade_entry.grade = payload.grade
        grade_entry.feedback_summary = payload.feedback_summary
        grade_entry.graded_by = teacher_id
        grade_entry.graded_at = datetime.now(timezone.utc)
    else:
        grade_entry = GradeEntry(
            submission_id=submission_id,
            marks_obtained=payload.marks_obtained,
            grade=payload.grade,
            feedback_summary=payload.feedback_summary,
            graded_by=teacher_id,
            graded_at=datetime.now(timezone.utc),
        )
        db.add(grade_entry)

    submission.status = SubmissionStatus.GRADED.value
    db.commit()
    db.refresh(grade_entry)
    return grade_entry


def get_gradebook(db: Session, class_id: str):
    assignments = db.query(Assignment).filter(Assignment.class_id == class_id).all()

    result = []
    for assignment in assignments:
        submissions = db.query(Submission).filter(Submission.assignment_id == assignment.id).all()
        graded = 0
        total_submissions = len(submissions)
        scores = []

        for submission in submissions:
            if submission.grade_entry:
                graded += 1
                scores.append(submission.grade_entry.marks_obtained)

        average_score = round(sum(scores) / len(scores), 2) if scores else 0

        result.append(
            {
                "assignment_id": assignment.id,
                "assignment_title": assignment.title,
                "class_id": assignment.class_id,
                "total_submissions": total_submissions,
                "graded_submissions": graded,
                "average_score": average_score,
            }
        )

    return result