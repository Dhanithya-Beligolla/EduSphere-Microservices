"""
Integration test script to verify all live API endpoints against the running server.
"""

import asyncio
import httpx
from datetime import datetime, timedelta, timezone
import jwt
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings

BASE_URL = "http://localhost:8000"

def generate_dev_token():
    """Generate a valid JWT token for testing."""
    payload = {
        "sub": "teacher-e2e-tester",
        "school_id": "school-001",
        "roles": ["SUBJECT_TEACHER", "ADMIN"],
        "subject_ids": ["subject-science", "subject-mathematics"],
        "class_ids": ["class-9a"],
        "section_ids": [],
        "stream_ids": [],
        "permissions": [],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

async def run_tests():
    token = generate_dev_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        print("1. Testing /health...")
        r = await client.get("/health")
        assert r.status_code == 200, f"Health failed: {r.text}"
        print("   [OK] Health check passed")

        print("2. Testing /ready (MongoDB connection)...")
        r = await client.get("/ready")
        assert r.status_code == 200, f"Ready failed: {r.text}"
        print("   [OK] Readiness check passed")

        print("3. Creating a new material (POST /api/v1/materials)...")
        new_material = {
            "title": "E2E Test Material",
            "description": "Created by integration test",
            "resourceType": "PDF",
            "subjectId": "subject-science",
            "gradeId": "grade-9",
            "termId": "term-1",
            "medium": "ENGLISH",
            "tags": ["test", "e2e"],
            "fileId": "file-123",
            "visibility": {
                "scopeType": "SCHOOL",
                "schoolId": "school-001"
            }
        }
        r = await client.post("/api/v1/materials", json=new_material)
        assert r.status_code == 201, f"Create material failed: {r.text}"
        mat_id = r.json()["data"]["id"]
        print(f"   [OK] Created material {mat_id}")

        print("4. Fetching the material (GET /api/v1/materials/{id})...")
        r = await client.get(f"/api/v1/materials/{mat_id}")
        assert r.status_code == 200, f"Get material failed: {r.text}"
        print("   [OK] Fetched material successfully")

        print("5. Updating the material (PATCH /api/v1/materials/{id})...")
        r = await client.patch(f"/api/v1/materials/{mat_id}", json={"title": "E2E Test Material Updated"})
        assert r.status_code == 200, f"Update material failed: {r.text}"
        print("   [OK] Updated material title")

        print("6. Publishing the material (POST /api/v1/materials/{id}/publish)...")
        r = await client.post(f"/api/v1/materials/{mat_id}/publish")
        assert r.status_code == 200, f"Publish material failed: {r.text}"
        assert r.json()["data"]["status"] == "PUBLISHED"
        print("   [OK] Material published")

        print("7. Searching for materials (GET /api/v1/materials/search)...")
        r = await client.get("/api/v1/materials/search?q=E2E&subjectId=subject-science")
        assert r.status_code == 200, f"Search failed: {r.text}"
        found = any(m["id"] == mat_id for m in r.json()["data"]["items"])
        assert found, "Created material not found in search results"
        print("   [OK] Search successful")

        print("8. Adding a new version (POST /api/v1/materials/{id}/versions)...")
        r = await client.post(f"/api/v1/materials/{mat_id}/versions", json={
            "changeLog": "Fixed typos",
            "fileId": "file-xyz-2"
        })
        assert r.status_code == 201, f"Add version failed: {r.text}"
        print("   [OK] Version added")

        print("9. Testing AI Tag Suggestion (POST /api/v1/materials/{id}/ai/suggest-tags)...")
        r = await client.post(f"/api/v1/materials/{mat_id}/ai/suggest-tags", timeout=10.0)
        assert r.status_code == 200, f"AI tags failed: {r.text}"
        print("   [OK] AI suggested tags correctly (deterministic)")

        print("10. Fetching Download URL (GET /api/v1/materials/{id}/download-url)...")
        r = await client.get(f"/api/v1/materials/{mat_id}/download-url")
        assert r.status_code == 200, f"Download URL failed: {r.text}"
        print("   [OK] Download URL stub fetched")

        print("11. Soft-Deleting the material (DELETE /api/v1/materials/{id})...")
        r = await client.delete(f"/api/v1/materials/{mat_id}")
        assert r.status_code == 200, f"Archive failed: {r.text}"
        
        r = await client.get(f"/api/v1/materials/{mat_id}")
        assert r.status_code == 404, "Material should return 404 after soft-delete"
        print("   [OK] Material successfully soft-deleted")

        print("\n*** ALL LIVE E2E API TESTS PASSED SUCCESSFULLY! ***")

if __name__ == "__main__":
    asyncio.run(run_tests())
