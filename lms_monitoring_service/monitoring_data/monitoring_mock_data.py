"""
monitoring_mock_data.py
-----------------------
Realistic in-memory mock data for a Sri Lankan school (SCH001).
All dashboards, reports, risk rules, audit logs, KPI snapshots,
intervention records and dashboard snapshots are stored here.
This module is the single source of truth consumed by every router.
"""

# ---------------------------------------------------------------------------
# PRINCIPAL DASHBOARD — whole-school KPIs visible to the school principal
# ---------------------------------------------------------------------------
PRINCIPAL_DASHBOARD = {
    "schoolId": "SCH001",
    "schoolName": "Royal National College — Kandy",
    "academicYear": "AY-2026",
    "termId": "TERM-1",
    "totalStudents": 1240,
    "totalTeachers": 87,
    "totalClasses": 42,
    "attendanceRate": 91.3,
    "atRiskStudentCount": 38,
    "sectionPerformance": [
        {
            "sectionId": "SEC-PRIMARY",
            "sectionName": "Primary Section (G1–G5)",
            "studentCount": 350,
            "avgAttendance": 94.1,
            "avgScore": 78.2,
            "atRisk": 5
        },
        {
            "sectionId": "SEC-JUNIOR",
            "sectionName": "Junior Secondary (G6–G9)",
            "studentCount": 380,
            "avgAttendance": 90.5,
            "avgScore": 68.7,
            "atRisk": 18
        },
        {
            "sectionId": "SEC-SENIOR",
            "sectionName": "Senior Secondary (G10–G11)",
            "studentCount": 290,
            "avgAttendance": 88.9,
            "avgScore": 65.4,
            "atRisk": 10
        },
        {
            "sectionId": "SEC-AL",
            "sectionName": "Advanced Level (G12–G13)",
            "studentCount": 220,
            "avgAttendance": 92.0,
            "avgScore": 71.8,
            "atRisk": 5
        }
    ],
    "recentAlerts": [
        {
            "alertId": "ALR-001",
            "type": "ATTENDANCE_DROP",
            "message": "Grade 09-A attendance dropped below 85 % this week",
            "severity": "HIGH",
            "createdAt": "2026-03-25T08:30:00Z"
        },
        {
            "alertId": "ALR-002",
            "type": "LOW_SUBMISSION",
            "message": "Only 52 % of Grade 08-B submitted the Mathematics assignment",
            "severity": "MEDIUM",
            "createdAt": "2026-03-24T14:15:00Z"
        },
        {
            "alertId": "ALR-003",
            "type": "TEACHER_INACTIVE",
            "message": "Teacher TCH-145 has not logged in for 7 days",
            "severity": "LOW",
            "createdAt": "2026-03-23T09:00:00Z"
        }
    ]
}

# ---------------------------------------------------------------------------
# SECTIONAL HEAD DASHBOARD — junior secondary section (SEC-JUNIOR)
# ---------------------------------------------------------------------------
SECTIONAL_HEAD_DASHBOARD = {
    "sectionId": "SEC-JUNIOR",
    "sectionName": "Junior Secondary (G6–G9)",
    "academicYear": "AY-2026",
    "termId": "TERM-1",
    "classList": [
        {
            "classId": "CLS-G06-A",
            "className": "Grade 6-A",
            "classTeacher": "Mrs. Perera",
            "studentCount": 38,
            "avgAttendance": 93.4,
            "avgSubmissionRate": 88.2
        },
        {
            "classId": "CLS-G07-A",
            "className": "Grade 7-A",
            "classTeacher": "Mr. Fernando",
            "studentCount": 40,
            "avgAttendance": 91.0,
            "avgSubmissionRate": 82.5
        },
        {
            "classId": "CLS-G08-A",
            "className": "Grade 8-A",
            "classTeacher": "Ms. Jayawardena",
            "studentCount": 37,
            "avgAttendance": 89.7,
            "avgSubmissionRate": 79.1
        },
        {
            "classId": "CLS-G09-A",
            "className": "Grade 9-A",
            "classTeacher": "Mr. Wickramasinghe",
            "studentCount": 36,
            "avgAttendance": 87.5,
            "avgSubmissionRate": 74.3
        }
    ],
    "teacherActivity": [
        {
            "teacherId": "TCH-230",
            "name": "Mr. Wickramasinghe",
            "lastLogin": "2026-03-25T07:45:00Z",
            "assignmentsCreated": 12,
            "materialsUploaded": 8,
            "gradesPublished": 45
        },
        {
            "teacherId": "TCH-112",
            "name": "Ms. De Silva",
            "lastLogin": "2026-03-25T08:20:00Z",
            "assignmentsCreated": 9,
            "materialsUploaded": 14,
            "gradesPublished": 38
        }
    ],
    "atRiskStudents": [
        {
            "studentId": "STU-3021",
            "name": "Kamal Jayasuriya",
            "classId": "CLS-G09-A",
            "riskLevel": "HIGH",
            "flags": ["LOW_SUBMISSION", "LOW_SCORE"]
        },
        {
            "studentId": "STU-3045",
            "name": "Nimesha Rathnayake",
            "classId": "CLS-G08-A",
            "riskLevel": "MEDIUM",
            "flags": ["LOW_ATTENDANCE"]
        },
        {
            "studentId": "STU-3078",
            "name": "Tharushi Bandara",
            "classId": "CLS-G09-A",
            "riskLevel": "HIGH",
            "flags": ["LOW_SUBMISSION", "LOW_ATTENDANCE"]
        }
    ]
}

# ---------------------------------------------------------------------------
# CLASS TEACHER DASHBOARD — Grade 9-A (CLS-G09-A)
# ---------------------------------------------------------------------------
CLASS_TEACHER_DASHBOARD = {
    "classId": "CLS-G09-A",
    "className": "Grade 9-A",
    "classTeacher": "Mr. Wickramasinghe",
    "academicYear": "AY-2026",
    "termId": "TERM-1",
    "studentCount": 36,
    "avgAttendance": 87.5,
    "subjectProgress": [
        {
            "subjectId": "SCI",
            "subjectName": "Science",
            "teacher": "Mr. Wickramasinghe",
            "avgScore": 64.8,
            "submissionRate": 74.3,
            "completedTopics": 8,
            "totalTopics": 12
        },
        {
            "subjectId": "MAT",
            "subjectName": "Mathematics",
            "teacher": "Ms. De Silva",
            "avgScore": 58.2,
            "submissionRate": 80.1,
            "completedTopics": 10,
            "totalTopics": 14
        },
        {
            "subjectId": "ENG",
            "subjectName": "English",
            "teacher": "Mrs. Cooray",
            "avgScore": 72.5,
            "submissionRate": 85.4,
            "completedTopics": 9,
            "totalTopics": 11
        },
        {
            "subjectId": "HIS",
            "subjectName": "History",
            "teacher": "Mr. Liyanage",
            "avgScore": 60.1,
            "submissionRate": 78.9,
            "completedTopics": 7,
            "totalTopics": 10
        }
    ],
    "attendanceTrend": [
        {"week": "W1", "rate": 92.0},
        {"week": "W2", "rate": 90.5},
        {"week": "W3", "rate": 88.3},
        {"week": "W4", "rate": 87.5}
    ],
    "studentHighlights": {
        "topPerformer": {
            "studentId": "STU-3002",
            "name": "Dilshan Herath",
            "avgScore": 92.4,
            "remark": "Consistently ranks first in all subjects"
        },
        "needsAttention": {
            "studentId": "STU-3021",
            "name": "Kamal Jayasuriya",
            "avgScore": 38.6,
            "remark": "Missing 40 % of assignments, attendance below 70 %"
        }
    }
}

# ---------------------------------------------------------------------------
# SUBJECT TEACHER DASHBOARD — Science (SCI) in CLS-G09-A
# ---------------------------------------------------------------------------
SUBJECT_TEACHER_DASHBOARD = {
    "classId": "CLS-G09-A",
    "subjectId": "SCI",
    "subjectName": "Science",
    "teacher": "Mr. Wickramasinghe",
    "academicYear": "AY-2026",
    "termId": "TERM-1",
    "assignmentStats": {
        "totalAssignments": 10,
        "published": 8,
        "drafts": 2,
        "avgSubmissionRate": 74.3,
        "avgScore": 64.8
    },
    "submissionRates": [
        {"assignmentId": "ASG-001", "title": "Photosynthesis Lab Report", "rate": 88.9},
        {"assignmentId": "ASG-002", "title": "Human Circulatory System Essay", "rate": 72.2},
        {"assignmentId": "ASG-003", "title": "Chemical Reactions Worksheet", "rate": 61.1},
        {"assignmentId": "ASG-004", "title": "Electricity & Magnetism Quiz", "rate": 80.6},
        {"assignmentId": "ASG-005", "title": "Ecosystem Project", "rate": 69.4}
    ],
    "gradeDistribution": {
        "A": 5,
        "B": 8,
        "C": 12,
        "S": 7,
        "W": 4
    },
    "topStudents": [
        {"studentId": "STU-3002", "name": "Dilshan Herath", "avgScore": 93.5},
        {"studentId": "STU-3010", "name": "Amaya Tennakoon", "avgScore": 89.2},
        {"studentId": "STU-3015", "name": "Sachini Weerasinghe", "avgScore": 86.7}
    ],
    "bottomStudents": [
        {"studentId": "STU-3021", "name": "Kamal Jayasuriya", "avgScore": 32.1},
        {"studentId": "STU-3034", "name": "Ruwan Pathirana", "avgScore": 40.5},
        {"studentId": "STU-3078", "name": "Tharushi Bandara", "avgScore": 42.8}
    ]
}

# ---------------------------------------------------------------------------
# ASSIGNMENT COMPLETION REPORT — TERM-1, totals by grade and subject
# ---------------------------------------------------------------------------
ASSIGNMENT_COMPLETION_REPORT = {
    "termId": "TERM-1",
    "academicYear": "AY-2026",
    "byGrade": [
        {"gradeId": "G07", "totalAssignments": 48, "submitted": 1680, "expected": 1920, "completionRate": 87.5},
        {"gradeId": "G08", "totalAssignments": 52, "submitted": 1750, "expected": 2080, "completionRate": 84.1},
        {"gradeId": "G09", "totalAssignments": 50, "submitted": 1440, "expected": 1800, "completionRate": 80.0},
        {"gradeId": "G10", "totalAssignments": 55, "submitted": 1870, "expected": 2200, "completionRate": 85.0}
    ],
    "bySubject": [
        {"subjectId": "SCI", "subjectName": "Science", "completionRate": 81.4},
        {"subjectId": "MAT", "subjectName": "Mathematics", "completionRate": 83.9},
        {"subjectId": "ENG", "subjectName": "English", "completionRate": 88.2},
        {"subjectId": "HIS", "subjectName": "History", "completionRate": 79.6}
    ]
}

# ---------------------------------------------------------------------------
# ACADEMIC RISK REPORT — at-risk students in Grade 09
# ---------------------------------------------------------------------------
ACADEMIC_RISK_REPORT = {
    "gradeId": "G09",
    "academicYear": "AY-2026",
    "termId": "TERM-1",
    "atRiskStudents": [
        {
            "studentId": "STU-3021",
            "name": "Kamal Jayasuriya",
            "classId": "CLS-G09-A",
            "riskLevel": "HIGH",
            "flags": ["LOW_SUBMISSION", "LOW_SCORE"],
            "submissionRate": 42.0,
            "avgScore": 38.6,
            "attendanceRate": 68.5
        },
        {
            "studentId": "STU-3078",
            "name": "Tharushi Bandara",
            "classId": "CLS-G09-A",
            "riskLevel": "HIGH",
            "flags": ["LOW_SUBMISSION", "LOW_ATTENDANCE"],
            "submissionRate": 55.0,
            "avgScore": 42.8,
            "attendanceRate": 62.3
        },
        {
            "studentId": "STU-3034",
            "name": "Ruwan Pathirana",
            "classId": "CLS-G09-A",
            "riskLevel": "MEDIUM",
            "flags": ["LOW_SCORE"],
            "submissionRate": 70.0,
            "avgScore": 40.5,
            "attendanceRate": 80.1
        },
        {
            "studentId": "STU-3090",
            "name": "Sanduni Perera",
            "classId": "CLS-G09-B",
            "riskLevel": "MEDIUM",
            "flags": ["LOW_ATTENDANCE"],
            "submissionRate": 78.0,
            "avgScore": 55.3,
            "attendanceRate": 65.0
        }
    ]
}

# ---------------------------------------------------------------------------
# MATERIAL USAGE REPORT — subject SCI
# ---------------------------------------------------------------------------
MATERIAL_USAGE_REPORT = {
    "subjectId": "SCI",
    "subjectName": "Science",
    "academicYear": "AY-2026",
    "termId": "TERM-1",
    "topMaterials": [
        {
            "materialId": "MAT-SCI-001",
            "title": "Photosynthesis — Animated Lesson (Sinhala)",
            "type": "VIDEO",
            "views": 320,
            "downloads": 185,
            "medium": "Sinhala"
        },
        {
            "materialId": "MAT-SCI-002",
            "title": "Human Body Systems — Interactive Diagram",
            "type": "INTERACTIVE",
            "views": 290,
            "downloads": 140,
            "medium": "English"
        },
        {
            "materialId": "MAT-SCI-003",
            "title": "Chemical Reactions Workbook — Tamil Medium",
            "type": "PDF",
            "views": 210,
            "downloads": 195,
            "medium": "Tamil"
        },
        {
            "materialId": "MAT-SCI-004",
            "title": "Electricity Basics — Sinhala Lecture Notes",
            "type": "PDF",
            "views": 180,
            "downloads": 160,
            "medium": "Sinhala"
        },
        {
            "materialId": "MAT-SCI-005",
            "title": "Ecosystem & Environment — English Slides",
            "type": "PRESENTATION",
            "views": 145,
            "downloads": 98,
            "medium": "English"
        }
    ],
    "byMedium": [
        {"medium": "Sinhala", "totalViews": 500, "totalDownloads": 345},
        {"medium": "Tamil", "totalViews": 210, "totalDownloads": 195},
        {"medium": "English", "totalViews": 435, "totalDownloads": 238}
    ]
}

# ---------------------------------------------------------------------------
# REPORT JOBS — populated at runtime when POST /report-jobs is called
# ---------------------------------------------------------------------------
REPORT_JOBS: dict = {}

# ---------------------------------------------------------------------------
# RISK RULES — pre-seeded detection rules
# ---------------------------------------------------------------------------
RISK_RULES: list = [
    {
        "ruleId": "RR-001",
        "name": "Low Submission Rate",
        "condition": "submissionRate < 60",
        "riskLevel": "HIGH",
        "active": True,
        "createdAt": "2026-01-15T10:00:00Z"
    },
    {
        "ruleId": "RR-002",
        "name": "Low Average Score",
        "condition": "avgScore < 50",
        "riskLevel": "HIGH",
        "active": True,
        "createdAt": "2026-01-15T10:05:00Z"
    }
]

# ---------------------------------------------------------------------------
# AUDIT LOGS — recent activity of user TCH-230
# ---------------------------------------------------------------------------
AUDIT_LOGS: list = [
    {
        "auditId": "AUD-001",
        "userId": "TCH-230",
        "action": "CREATE_ASSIGNMENT",
        "resource": "ASG-005 — Ecosystem Project",
        "timestamp": "2026-03-20T09:15:00Z",
        "ipAddress": "192.168.1.42"
    },
    {
        "auditId": "AUD-002",
        "userId": "TCH-230",
        "action": "GRADE_SUBMISSION",
        "resource": "ASG-001 — Photosynthesis Lab Report (STU-3002)",
        "timestamp": "2026-03-21T11:30:00Z",
        "ipAddress": "192.168.1.42"
    },
    {
        "auditId": "AUD-003",
        "userId": "TCH-230",
        "action": "UPLOAD_MATERIAL",
        "resource": "MAT-SCI-004 — Electricity Basics Sinhala Lecture Notes",
        "timestamp": "2026-03-22T08:45:00Z",
        "ipAddress": "192.168.1.42"
    },
    {
        "auditId": "AUD-004",
        "userId": "TCH-230",
        "action": "PUBLISH_ASSIGNMENT",
        "resource": "ASG-004 — Electricity & Magnetism Quiz",
        "timestamp": "2026-03-22T14:00:00Z",
        "ipAddress": "192.168.1.42"
    },
    {
        "auditId": "AUD-005",
        "userId": "TCH-230",
        "action": "VIEW_DASHBOARD",
        "resource": "Subject Teacher Dashboard — SCI / CLS-G09-A",
        "timestamp": "2026-03-24T07:50:00Z",
        "ipAddress": "192.168.1.42"
    },
    {
        "auditId": "AUD-006",
        "userId": "TCH-230",
        "action": "EXPORT_REPORT",
        "resource": "Assignment Completion Report — TERM-1 (PDF)",
        "timestamp": "2026-03-25T10:20:00Z",
        "ipAddress": "192.168.1.42"
    }
]

# ---------------------------------------------------------------------------
# KPI SNAPSHOTS — school-wide key performance indicators
# ---------------------------------------------------------------------------
KPI_SNAPSHOTS: list = [
    {
        "kpiId": "KPI-001",
        "name": "Overall Attendance Rate",
        "value": 91.3,
        "unit": "%",
        "trend": "DOWN",
        "comparedToPreviousTerm": -1.2
    },
    {
        "kpiId": "KPI-002",
        "name": "Assignment Completion Rate",
        "value": 84.2,
        "unit": "%",
        "trend": "UP",
        "comparedToPreviousTerm": 2.5
    },
    {
        "kpiId": "KPI-003",
        "name": "Average Academic Score",
        "value": 67.8,
        "unit": "marks",
        "trend": "STABLE",
        "comparedToPreviousTerm": 0.3
    },
    {
        "kpiId": "KPI-004",
        "name": "At-Risk Student Count",
        "value": 38,
        "unit": "students",
        "trend": "UP",
        "comparedToPreviousTerm": 5
    },
    {
        "kpiId": "KPI-005",
        "name": "Teacher Platform Engagement",
        "value": 78.5,
        "unit": "%",
        "trend": "UP",
        "comparedToPreviousTerm": 4.1
    }
]

# ---------------------------------------------------------------------------
# INTERVENTION QUEUE — records for at-risk student follow-ups
# ---------------------------------------------------------------------------
INTERVENTION_QUEUE: list = [
    {
        "interventionId": "INT-001",
        "studentId": "STU-3021",
        "classId": "CLS-G09-A",
        "reason": "Submission rate 42 %, average score 38.6 — needs immediate academic support",
        "assignedTo": "TCH-230",
        "status": "IN_PROGRESS",
        "createdAt": "2026-03-18T09:00:00Z",
        "notes": "Parent meeting scheduled for 2026-03-28"
    },
    {
        "interventionId": "INT-002",
        "studentId": "STU-3078",
        "classId": "CLS-G09-A",
        "reason": "Attendance 62.3 %, submission rate 55 % — chronic absenteeism risk",
        "assignedTo": "TCH-230",
        "status": "OPEN",
        "createdAt": "2026-03-19T10:30:00Z",
        "notes": None
    },
    {
        "interventionId": "INT-003",
        "studentId": "STU-3034",
        "classId": "CLS-G09-A",
        "reason": "Average score 40.5 across all subjects — additional tutoring recommended",
        "assignedTo": "TCH-112",
        "status": "OPEN",
        "createdAt": "2026-03-20T08:15:00Z",
        "notes": None
    },
    {
        "interventionId": "INT-004",
        "studentId": "STU-3090",
        "classId": "CLS-G09-B",
        "reason": "Attendance dropped to 65 % — potential family issue flagged by class teacher",
        "assignedTo": "TCH-305",
        "status": "IN_PROGRESS",
        "createdAt": "2026-03-21T11:00:00Z",
        "notes": "Home visit completed; student returning next week"
    }
]

# ---------------------------------------------------------------------------
# DASHBOARD SNAPSHOTS — periodic saved snapshots of dashboards
# ---------------------------------------------------------------------------
DASHBOARD_SNAPSHOTS: list = [
    {
        "snapshotId": "SNAP-001",
        "role": "PRINCIPAL",
        "generatedAt": "2026-03-25T06:00:00Z",
        "summary": {
            "totalStudents": 1240,
            "avgAttendance": 91.3,
            "atRiskCount": 38,
            "alertCount": 3
        }
    },
    {
        "snapshotId": "SNAP-002",
        "role": "SECTIONAL_HEAD",
        "generatedAt": "2026-03-25T06:05:00Z",
        "summary": {
            "sectionId": "SEC-JUNIOR",
            "classCount": 4,
            "avgSubmissionRate": 81.0,
            "atRiskCount": 3
        }
    },
    {
        "snapshotId": "SNAP-003",
        "role": "CLASS_TEACHER",
        "generatedAt": "2026-03-25T06:10:00Z",
        "summary": {
            "classId": "CLS-G09-A",
            "studentCount": 36,
            "avgAttendance": 87.5,
            "avgScore": 63.9
        }
    }
]
