"""
Enum constants used across the Learning Materials service.
"""

from enum import Enum


class MaterialStatus(str, Enum):
    """Lifecycle states for a learning material."""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class ResourceType(str, Enum):
    """Types of learning resources."""
    PDF = "PDF"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    LINK = "LINK"
    DOC = "DOC"
    PPT = "PPT"
    WORKSHEET = "WORKSHEET"
    PAST_PAPER = "PAST_PAPER"
    REVISION_PACK = "REVISION_PACK"


class Medium(str, Enum):
    """Teaching medium / language of instruction."""
    SINHALA = "SINHALA"
    TAMIL = "TAMIL"
    ENGLISH = "ENGLISH"


class VisibilityScopeType(str, Enum):
    """Scope of material visibility."""
    SCHOOL = "SCHOOL"
    SECTION = "SECTION"
    STREAM = "STREAM"
    GRADE = "GRADE"
    CLASS = "CLASS"
    SUBJECT = "SUBJECT"


class Role(str, Enum):
    """Roles recognized by the authorization model."""
    PRINCIPAL = "PRINCIPAL"
    DEPUTY_PRINCIPAL = "DEPUTY_PRINCIPAL"
    SECTIONAL_HEAD = "SECTIONAL_HEAD"
    CLASS_TEACHER = "CLASS_TEACHER"
    SUBJECT_TEACHER = "SUBJECT_TEACHER"
    STUDENT = "STUDENT"
    PARENT = "PARENT"
    ADMIN = "ADMIN"


class Permission(str, Enum):
    """Granular permission identifiers."""
    MATERIAL_CREATE = "material:create"
    MATERIAL_READ = "material:read"
    MATERIAL_UPDATE = "material:update"
    MATERIAL_DELETE = "material:delete"
    MATERIAL_PUBLISH = "material:publish"
    MATERIAL_MANAGE = "material:manage"


# Roles with full management access
ADMIN_ROLES = {Role.ADMIN, Role.PRINCIPAL}

# Roles allowed to create/update materials
WRITE_ROLES = {
    Role.ADMIN, Role.PRINCIPAL, Role.DEPUTY_PRINCIPAL,
    Role.SECTIONAL_HEAD, Role.CLASS_TEACHER, Role.SUBJECT_TEACHER,
}

# Roles allowed to read materials (all roles)
READ_ROLES = {role for role in Role}
