from fastapi import APIRouter
from app.api.v1.endpoints import assignments, submissions, grading, results

api_router = APIRouter()
api_router.include_router(assignments.router)
api_router.include_router(submissions.router)
api_router.include_router(grading.router)
api_router.include_router(results.router)