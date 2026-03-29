from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_roles
from app.schemas.common import StandardResponse
from app.services import result_service

router = APIRouter(prefix="/results", tags=["Results"])


@router.post("/{submission_id}/publish", response_model=StandardResponse)
def publish_result(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("SUBJECT_TEACHER", "CLASS_TEACHER")),
):
    result = result_service.publish_result(db, submission_id, current_user["id"])
    return StandardResponse(
        message="Result published successfully",
        data={
            "submission_id": result.submission_id,
            "is_published": result.is_published,
            "published_at": result.published_at,
        },
    )


@router.get("/student/{student_id}", response_model=StandardResponse)
def list_student_results(
    student_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    results = result_service.list_student_results(
        db, student_id, current_user["id"], current_user["role"]
    )
    return StandardResponse(
        message="Student results fetched successfully",
        data=results,
    )