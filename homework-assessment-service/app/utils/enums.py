from enum import Enum


class AssignmentType(str, Enum):
    HOMEWORK = "HOMEWORK"
    QUIZ = "QUIZ"
    ASSESSMENT = "ASSESSMENT"


class AssignmentStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"


class SubmissionStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    RESUBMITTED = "RESUBMITTED"
    GRADED = "GRADED"


class LanguageMedium(str, Enum):
    ENGLISH = "ENGLISH"
    SINHALA = "SINHALA"
    TAMIL = "TAMIL"