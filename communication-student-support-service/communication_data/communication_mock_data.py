from datetime import datetime, timedelta
import uuid

# --- Mock Data Storage ---

# Role-based users for reference:
# Principal: PR_01
# Sectional Head: SH_01 (Middle School)
# Teacher: T_01 (Grade 10-A)
# Student: S_01 (Praveen Perera)
# Parent: P_01 (Mr. Perera)

NOTICES = [
    {
        "id": "N_001",
        "title": "Avurudu Celebrations 2026",
        "content": "The annual school Avurudu celebrations will be held on April 10th. All students to wear traditional attire.",
        "audience": "ALL",
        "status": "PUBLISHED",
        "created_at": datetime(2026, 3, 20, 9, 0),
        "published_at": datetime(2026, 3, 22, 10, 0),
        "author_id": "PR_01",
        "author_role": "Principal"
    },
    {
        "id": "N_002",
        "title": "1st Term Test Schedule",
        "content": "The 1st term tests for Middle School will commence from March 30th. Please check the notice board for the timetable.",
        "audience": "SECTION_MIDDLE",
        "status": "PUBLISHED",
        "created_at": datetime(2026, 3, 15, 8, 30),
        "published_at": datetime(2026, 3, 16, 14, 0),
        "author_id": "SH_01",
        "author_role": "Sectional Head"
    },
    {
        "id": "N_003",
        "title": "Staff Meeting: Curriculum Review",
        "content": "Mandatory staff meeting for all teachers this Friday at 2:00 PM in the auditorium.",
        "audience": "STAFF",
        "status": "DRAFT",
        "created_at": datetime(2026, 3, 25, 11, 0),
        "published_at": None,
        "author_id": "PR_01",
        "author_role": "Principal"
    }
]

MESSAGES = [
    {
        "id": "M_001",
        "sender_id": "T_01",
        "receiver_id": "S_01",
        "content": "Praveen, remember to submit your science assignment by tonight.",
        "timestamp": datetime(2026, 3, 26, 16, 0),
        "conversation_id": "CONV_001"
    },
    {
        "id": "M_002",
        "sender_id": "S_01",
        "receiver_id": "T_01",
        "content": "Yes Sir, I am just finishing it up. Will submit via the portal.",
        "timestamp": datetime(2026, 3, 26, 16, 15),
        "conversation_id": "CONV_001"
    },
    {
        "id": "M_003",
        "sender_id": "T_01",
        "receiver_id": "P_01",
        "content": "Dear Mr. Perera, Praveen's attendance has been slightly irregular this week. Please check.",
        "timestamp": datetime(2026, 3, 24, 10, 0),
        "conversation_id": "CONV_002"
    }
]

ALERTS = [
    {
        "id": "A_001",
        "user_id": "S_01",
        "type": "ASSIGNMENT",
        "title": "Assignment Missed!",
        "message": "You have missed the deadline for History Assignment 02.",
        "priority": "HIGH",
        "is_read": False,
        "created_at": datetime(2026, 3, 25, 9, 0)
    },
    {
        "id": "A_002",
        "user_id": "S_01",
        "type": "ATTENDANCE",
        "title": "Low Attendance Alert",
        "message": "Your attendance for March is below 80%. Please meet your class teacher.",
        "priority": "MEDIUM",
        "is_read": True,
        "created_at": datetime(2026, 3, 20, 8, 0)
    }
]

SUPPORT_CASES = [
    {
        "id": "SC_001",
        "student_id": "S_01",
        "subject": "Difficulty in Mathematics",
        "description": "Student reports struggling with Calculus concepts and feels overwhelmed.",
        "status": "IN_PROGRESS",
        "assigned_staff_id": "COUNSELOR_01",
        "created_at": datetime(2026, 3, 10, 10, 0),
        "updated_at": datetime(2026, 3, 12, 11, 0),
        "notes": "Had first session. Student needs extra remedial support."
    }
]
