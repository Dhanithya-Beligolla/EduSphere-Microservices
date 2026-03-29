"""
Test data factories for generating sample materials, versions, and tokens.
"""

from typing import Any


def make_material_data(
    title: str = "Grade 9 Science Revision Notes",
    description: str = "Comprehensive revision notes for Grade 9 Science Term 1",
    resource_type: str = "PDF",
    subject_id: str = "subject-science",
    grade_id: str = "grade-9",
    term_id: str = "term-1",
    medium: str = "ENGLISH",
    **overrides: Any,
) -> dict[str, Any]:
    """Create sample material request data."""
    data = {
        "title": title,
        "description": description,
        "resourceType": resource_type,
        "subjectId": subject_id,
        "gradeId": grade_id,
        "termId": term_id,
        "medium": medium,
        "tags": ["science", "revision", "grade-9"],
        "fileId": "file-abc-123",
        "visibility": {
            "scopeType": "SCHOOL",
            "schoolId": "school-001",
            "sectionIds": [],
            "streamIds": [],
            "gradeIds": ["grade-9"],
            "classIds": [],
            "subjectIds": ["subject-science"],
        },
    }
    data.update(overrides)
    return data


def make_link_material_data(**overrides: Any) -> dict[str, Any]:
    """Create sample link-type material data."""
    data = make_material_data(
        title="Khan Academy - Grade 9 Physics",
        resource_type="LINK",
        **overrides,
    )
    data.pop("fileId", None)
    data["externalUrl"] = "https://www.khanacademy.org/science/physics"
    return data


def make_version_data(
    change_log: str = "Updated diagrams and corrected page 12",
    file_id: str = "file-xyz-456",
    **overrides: Any,
) -> dict[str, Any]:
    """Create sample version request data."""
    data = {
        "changeLog": change_log,
        "fileId": file_id,
    }
    data.update(overrides)
    return data


def make_sri_lankan_materials() -> list[dict[str, Any]]:
    """Generate a set of sample Sri Lankan school materials for seed data."""
    return [
        make_material_data(
            title="Grade 9 Science Revision Notes - Term 1",
            description="Complete revision notes covering all units for Grade 9 Science",
            resource_type="PDF",
            subject_id="subject-science",
            grade_id="grade-9",
            term_id="term-1",
            medium="ENGLISH",
            tags=["science", "revision", "grade-9", "english-medium"],
        ),
        make_material_data(
            title="Grade 10 Mathematics Worksheet - Algebra",
            description="Practice worksheet for algebraic expressions and equations",
            resource_type="WORKSHEET",
            subject_id="subject-mathematics",
            grade_id="grade-10",
            term_id="term-2",
            medium="SINHALA",
            tags=["mathematics", "algebra", "worksheet", "grade-10"],
        ),
        make_material_data(
            title="O/L Science Past Paper 2024",
            description="2024 O/L Science past paper with marking scheme",
            resource_type="PAST_PAPER",
            subject_id="subject-science",
            grade_id="grade-11",
            medium="ENGLISH",
            tags=["o-level", "past-paper", "science", "2024"],
        ),
        make_material_data(
            title="Grade 8 History Presentation - Ancient Sri Lanka",
            description="PowerPoint presentation on ancient Sri Lankan civilizations",
            resource_type="PPT",
            subject_id="subject-history",
            grade_id="grade-8",
            term_id="term-1",
            medium="SINHALA",
            tags=["history", "presentation", "ancient-sri-lanka"],
        ),
        make_link_material_data(
            title="Grade 9 Physics Video - Motion and Forces",
            description="Educational video explaining Newton's laws of motion",
            subject_id="subject-science",
            grade_id="grade-9",
            term_id="term-2",
            medium="ENGLISH",
            tags=["physics", "video", "motion", "forces"],
        ),
    ]
