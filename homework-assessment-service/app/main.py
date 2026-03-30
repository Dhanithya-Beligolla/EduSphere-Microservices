import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.api import api_router
from app.core.config import settings

os.makedirs(settings.upload_dir, exist_ok=True)

app = FastAPI(
    title="Homework & Assessment Service",
    version="1.0.0",
    description="FastAPI MVP for LMS homework and assessment microservice",
)

app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "Homework assessment service is healthy",
        "data": {"service": settings.app_name},
    }


app.include_router(api_router, prefix=settings.api_v1_prefix)