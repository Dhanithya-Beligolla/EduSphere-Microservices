from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate
from app.services.academic_client import validate_teacher_assignment
from app.utils.enums import AssignmentStatus

async def create_assignment(db: Session, payload: AssignmentCreate, teacher_id: str):
    if payload.publish_at and payload.due_at <= payload.publish_at:
        raise HTTPException(status_code=400, detail="Due date must be after publish date")

    await validate_teacher_assignment(teacher_id, payload.class_id, payload.subject_id)

    assignment = Assignment(
        title=payload.title,
        description=payload.description,
        type=payload.type.value,
        class_id=payload.class_id,
        subject_id=payload.subject_id,
        teacher_id=teacher_id,
        publish_at=payload.publish_at,
        due_at=payload.due_at,
        total_marks=payload.total_marks,
        allow_late_submission=payload.allow_late_submission,
        max_attempts=payload.max_attempts,
        language_medium=payload.language_medium.value if payload.language_medium else None,
        status=AssignmentStatus.DRAFT.value,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def list_assignments(db: Session, role: str, user_id: str, class_id: str | None = None, student_id: str | None = None):
    query = db.query(Assignment)

    if class_id:
        query = query.filter(Assignment.class_id == class_id)

    if role in ["SUBJECT_TEACHER", "CLASS_TEACHER"]:
        query = query.filter(Assignment.teacher_id == user_id)

    if role == "STUDENT" and student_id:
        query = query.filter(Assignment.status == AssignmentStatus.PUBLISHED.value)

    return query.order_by(Assignment.created_at.desc()).all()


def get_assignment(db: Session, assignment_id: int):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


async def update_assignment(db: Session, assignment_id: int, payload: AssignmentUpdate, current_user_id: str):
    assignment = get_assignment(db, assignment_id)

    if assignment.teacher_id != current_user_id:
        raise HTTPException(status_code=403, detail="Only the creator can update this assignment")

    if assignment.status == AssignmentStatus.CLOSED.value:
        raise HTTPException(status_code=409, detail="Closed assignments cannot be updated")

    update_data = payload.model_dump(exclude_unset=True)

    if "due_at" in update_data and assignment.publish_at and update_data["due_at"] <= assignment.publish_at:
        raise HTTPException(status_code=400, detail="Due date must be after publish date")

    for key, value in update_data.items():
        if hasattr(value, "value"):
            value = value.value
        setattr(assignment, key, value)

    db.commit()
    db.refresh(assignment)
    return assignment


def publish_assignment(db: Session, assignment_id: int, current_user_id: str):
    assignment = get_assignment(db, assignment_id)

    if assignment.teacher_id != current_user_id:
        raise HTTPException(status_code=403, detail="Only the creator can publish this assignment")

    assignment.status = AssignmentStatus.PUBLISHED.value
    db.commit()
    db.refresh(assignment)
    return assignment