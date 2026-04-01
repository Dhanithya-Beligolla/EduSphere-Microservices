"""
Seed script — populates the database with sample Sri Lankan school data.

Usage:
    python -m scripts.seed

Requires MongoDB to be running and .env to be configured.
"""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Load settings
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings


SAMPLE_MATERIALS = [
    {
        "title": "Grade 9 Science Revision Notes - Term 1",
        "description": "Comprehensive revision notes covering Matter and Energy, Living World, and Earth Science for Grade 9 students. Includes diagrams, key concepts, and practice questions.",
        "subjectId": "subject-science",
        "gradeId": "grade-9",
        "termId": "term-1",
        "unitId": "unit-matter-energy",
        "medium": "ENGLISH",
        "resourceType": "PDF",
        "tags": ["science", "revision", "grade-9", "english-medium", "term-1", "notes"],
        "status": "PUBLISHED",
        "visibility": {
            "scopeType": "SCHOOL",
            "schoolId": "school-001",
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": ["grade-9"],
            "classIds": [],
            "subjectIds": ["subject-science"],
        },
        "currentVersion": 2,
        "fileId": "file-rev-notes-001",
        "externalUrl": None,
        "thumbnailUrl": None,
        "language": "en",
        "schoolId": "school-001",
        "publishedAt": datetime(2026, 2, 15, 8, 0, 0),
        "publishedBy": "teacher-kumara",
        "createdAt": datetime(2026, 1, 10, 10, 30, 0),
        "createdBy": "teacher-kumara",
        "updatedAt": datetime(2026, 2, 15, 8, 0, 0),
        "updatedBy": "teacher-kumara",
        "archivedAt": None,
        "archivedBy": None,
        "isDeleted": False,
    },
    {
        "title": "ශ්‍රේණිය 10 ගණිතය - වීජ ගණිතය වැඩ පත්‍රිකාව",
        "description": "වීජ ප්‍රකාශන සහ සමීකරණ පිළිබඳ පුහුණු වැඩ පත්‍රිකාව. 50+ ගැටලු ඇතුළත් වේ.",
        "subjectId": "subject-mathematics",
        "gradeId": "grade-10",
        "termId": "term-2",
        "unitId": "unit-algebra",
        "medium": "SINHALA",
        "resourceType": "WORKSHEET",
        "tags": ["mathematics", "algebra", "worksheet", "grade-10", "sinhala-medium"],
        "status": "PUBLISHED",
        "visibility": {
            "scopeType": "GRADE",
            "schoolId": "school-001",
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": ["grade-10"],
            "classIds": [],
            "subjectIds": ["subject-mathematics"],
        },
        "currentVersion": 1,
        "fileId": "file-worksheet-002",
        "externalUrl": None,
        "thumbnailUrl": None,
        "language": "si",
        "schoolId": "school-001",
        "publishedAt": datetime(2026, 3, 1, 9, 0, 0),
        "publishedBy": "teacher-perera",
        "createdAt": datetime(2026, 2, 20, 14, 0, 0),
        "createdBy": "teacher-perera",
        "updatedAt": datetime(2026, 3, 1, 9, 0, 0),
        "updatedBy": "teacher-perera",
        "archivedAt": None,
        "archivedBy": None,
        "isDeleted": False,
    },
    {
        "title": "O/L Science Past Paper 2024 with Marking Scheme",
        "description": "Official 2024 O/L Science paper with detailed marking scheme and model answers. Both Paper I (MCQ) and Paper II (Structured/Essay) included.",
        "subjectId": "subject-science",
        "gradeId": "grade-11",
        "termId": None,
        "unitId": None,
        "medium": "ENGLISH",
        "resourceType": "PAST_PAPER",
        "tags": ["o-level", "past-paper", "science", "2024", "marking-scheme", "exam-prep"],
        "status": "PUBLISHED",
        "visibility": {
            "scopeType": "SCHOOL",
            "schoolId": "school-001",
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": ["grade-10", "grade-11"],
            "classIds": [],
            "subjectIds": ["subject-science"],
        },
        "currentVersion": 1,
        "fileId": "file-pastpaper-003",
        "externalUrl": None,
        "thumbnailUrl": None,
        "language": "en",
        "schoolId": "school-001",
        "publishedAt": datetime(2026, 1, 5, 12, 0, 0),
        "publishedBy": "teacher-kumara",
        "createdAt": datetime(2026, 1, 3, 16, 30, 0),
        "createdBy": "teacher-kumara",
        "updatedAt": datetime(2026, 1, 5, 12, 0, 0),
        "updatedBy": "teacher-kumara",
        "archivedAt": None,
        "archivedBy": None,
        "isDeleted": False,
    },
    {
        "title": "Grade 8 History - Ancient Sri Lankan Civilizations",
        "description": "Interactive presentation covering Anuradhapura Kingdom, Polonnaruwa, Sigiriya, and ancient hydraulic civilizations. Includes maps, timelines, and archaeological evidence.",
        "subjectId": "subject-history",
        "gradeId": "grade-8",
        "termId": "term-1",
        "unitId": "unit-ancient-lanka",
        "medium": "SINHALA",
        "resourceType": "PPT",
        "tags": ["history", "presentation", "ancient-sri-lanka", "anuradhapura", "grade-8"],
        "status": "DRAFT",
        "visibility": {
            "scopeType": "CLASS",
            "schoolId": "school-001",
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": ["grade-8"],
            "classIds": ["class-8a", "class-8b"],
            "subjectIds": ["subject-history"],
        },
        "currentVersion": 1,
        "fileId": "file-ppt-004",
        "externalUrl": None,
        "thumbnailUrl": None,
        "language": "si",
        "schoolId": "school-001",
        "publishedAt": None,
        "publishedBy": None,
        "createdAt": datetime(2026, 3, 20, 11, 0, 0),
        "createdBy": "teacher-fernando",
        "updatedAt": datetime(2026, 3, 20, 11, 0, 0),
        "updatedBy": "teacher-fernando",
        "archivedAt": None,
        "archivedBy": None,
        "isDeleted": False,
    },
    {
        "title": "Grade 9 Physics - Motion and Forces (Video)",
        "description": "Educational video explaining Newton's laws of motion with real-world examples. Covers: displacement, velocity, acceleration, force, and momentum.",
        "subjectId": "subject-science",
        "gradeId": "grade-9",
        "termId": "term-2",
        "unitId": "unit-motion-forces",
        "medium": "ENGLISH",
        "resourceType": "LINK",
        "tags": ["physics", "video", "motion", "forces", "newton", "grade-9"],
        "status": "PUBLISHED",
        "visibility": {
            "scopeType": "SCHOOL",
            "schoolId": "school-001",
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": ["grade-9"],
            "classIds": [],
            "subjectIds": ["subject-science"],
        },
        "currentVersion": 1,
        "fileId": None,
        "externalUrl": "https://www.khanacademy.org/science/physics/forces-newtons-laws",
        "thumbnailUrl": None,
        "language": "en",
        "schoolId": "school-001",
        "publishedAt": datetime(2026, 3, 10, 7, 30, 0),
        "publishedBy": "teacher-kumara",
        "createdAt": datetime(2026, 3, 8, 16, 0, 0),
        "createdBy": "teacher-kumara",
        "updatedAt": datetime(2026, 3, 10, 7, 30, 0),
        "updatedBy": "teacher-kumara",
        "archivedAt": None,
        "archivedBy": None,
        "isDeleted": False,
    },
    {
        "title": "தரம் 9 அறிவியல் பரிசோதனை கையேடு",
        "description": "தரம் 9 அறிவியல் பாடத்திற்கான பரிசோதனை கையேடு. அனைத்து கால பரிசோதனைகளும் உள்ளடக்கப்பட்டுள்ளன.",
        "subjectId": "subject-science",
        "gradeId": "grade-9",
        "termId": "term-1",
        "unitId": None,
        "medium": "TAMIL",
        "resourceType": "PDF",
        "tags": ["science", "practical", "lab-manual", "grade-9", "tamil-medium"],
        "status": "PUBLISHED",
        "visibility": {
            "scopeType": "SCHOOL",
            "schoolId": "school-001",
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": ["grade-9"],
            "classIds": [],
            "subjectIds": ["subject-science"],
        },
        "currentVersion": 1,
        "fileId": "file-lab-manual-006",
        "externalUrl": None,
        "thumbnailUrl": None,
        "language": "ta",
        "schoolId": "school-001",
        "publishedAt": datetime(2026, 2, 28, 10, 0, 0),
        "publishedBy": "teacher-nadesan",
        "createdAt": datetime(2026, 2, 25, 13, 30, 0),
        "createdBy": "teacher-nadesan",
        "updatedAt": datetime(2026, 2, 28, 10, 0, 0),
        "updatedBy": "teacher-nadesan",
        "archivedAt": None,
        "archivedBy": None,
        "isDeleted": False,
    },
]

SAMPLE_VERSIONS = [
    {
        "materialId": None,  # Will be set to first material's ID
        "versionNumber": 1,
        "fileId": "file-rev-notes-001-v1",
        "changeLog": "Initial upload of revision notes",
        "createdAt": datetime(2026, 1, 10, 10, 30, 0),
        "createdBy": "teacher-kumara",
    },
    {
        "materialId": None,
        "versionNumber": 2,
        "fileId": "file-rev-notes-001",
        "changeLog": "Updated diagrams in Chapter 3, added practice questions",
        "createdAt": datetime(2026, 2, 14, 15, 0, 0),
        "createdBy": "teacher-kumara",
    },
]


async def seed():
    """Insert sample data into MongoDB."""
    print(f"Connecting to MongoDB: {settings.mongo_uri}")
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.mongo_db_name]

    # Clear existing data
    await db["learning_materials"].delete_many({})
    await db["material_versions"].delete_many({})
    print("Cleared existing data")

    # Insert materials
    materials_collection = db["learning_materials"]
    inserted_ids = []
    for material in SAMPLE_MATERIALS:
        result = await materials_collection.insert_one(material)
        inserted_ids.append(result.inserted_id)
        print(f"  ✓ Inserted: {material['title'][:60]}...")

    # Insert versions for first material
    versions_collection = db["material_versions"]
    for version in SAMPLE_VERSIONS:
        version["materialId"] = str(inserted_ids[0])
        await versions_collection.insert_one(version)
        print(f"  ✓ Version {version['versionNumber']}: {version['changeLog'][:50]}...")

    print(f"\n✅ Seeded {len(SAMPLE_MATERIALS)} materials and {len(SAMPLE_VERSIONS)} versions")

    # Create indexes
    from app.db.indexes import create_indexes
    await create_indexes(db)
    print("✅ Indexes created")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
