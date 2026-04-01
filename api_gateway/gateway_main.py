"""
API Gateway entrypoint.

Run with:
    uvicorn gateway_main:app --reload --port 8080
"""

from app.main import app
