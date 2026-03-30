from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_roles
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentOut
from app.schemas.common import StandardResponse
from app.services import assignment_service

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.post("", response_model=StandardResponse)
async def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("SUBJECT_TEACHER", "CLASS_TEACHER")),
):
    assignment = await assignment_service.create_assignment(db, payload, current_user["id"])
    return StandardResponse(message="Assignment created successfully", data=AssignmentOut.model_validate(assignment))


@router.get("", response_model=StandardResponse)
async def list_assignments(
    class_id: str | None = Query(default=None),
    student_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    assignments = assignment_service.list_assignments(db, current_user["role"], current_user["id"], class_id, student_id)
    return StandardResponse(
        message="Assignments fetched successfully",
        data=[AssignmentOut.model_validate(item) for item in assignments],
    )


@router.get("/{assignment_id}", response_model=StandardResponse)
def get_assignment(assignment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    assignment = assignment_service.get_assignment(db, assignment_id)
    return StandardResponse(message="Assignment fetched successfully", data=AssignmentOut.model_validate(assignment))


@router.patch("/{assignment_id}", response_model=StandardResponse)
async def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("SUBJECT_TEACHER", "CLASS_TEACHER")),
):
    assignment = await assignment_service.update_assignment(db, assignment_id, payload, current_user["id"])
    return StandardResponse(message="Assignment updated successfully", data=AssignmentOut.model_validate(assignment))


@router.post("/{assignment_id}/publish", response_model=StandardResponse)
def publish_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("SUBJECT_TEACHER", "CLASS_TEACHER")),
):
    assignment = assignment_service.publish_assignment(db, assignment_id, current_user["id"])
    return StandardResponse(message="Assignment published successfully", data=AssignmentOut.model_validate(assignment))