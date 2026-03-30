"""
Central API router registry.
All route modules are registered here with their prefixes.
"""

from fastapi import APIRouter

from app.api.routes import health, materials, versions, visibility, download, search, analytics, ai_tools

api_router = APIRouter()

# System routes — no prefix
api_router.include_router(health.router, tags=["System"])

# v1 resource routes
api_router.include_router(search.router, prefix="/api/v1/materials", tags=["Search"])
api_router.include_router(materials.router, prefix="/api/v1/materials", tags=["Materials"])
api_router.include_router(versions.router, prefix="/api/v1/materials", tags=["Versions"])
api_router.include_router(visibility.router, prefix="/api/v1/materials", tags=["Visibility"])
api_router.include_router(download.router, prefix="/api/v1/materials", tags=["Download"])
api_router.include_router(analytics.router, prefix="/api/v1/materials", tags=["Analytics"])
api_router.include_router(ai_tools.router, prefix="/api/v1/materials", tags=["AI Tools"])
