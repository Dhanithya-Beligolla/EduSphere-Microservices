from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Any
from datetime import datetime
import uuid

# --- Base Response Schema ---

class ResponseMeta(BaseModel):
    requestId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    version: str = "v1"

class APIResponse(BaseModel):
    data: Any
    meta: ResponseMeta = Field(default_factory=ResponseMeta)
    errors: List[str] = []

# --- Notice Schemas ---

class NoticeCreate(BaseModel):
    title: str
    content: str
    audience: str  # e.g., "ALL", "SECTION_PRIMARY", "SECTION_SECONDARY", "STAFF"
    author_id: str
    author_role: str

class Notice(BaseModel):
    id: str
    title: str
    content: str
    audience: str
    status: str  # "DRAFT", "PUBLISHED"
    created_at: datetime
    published_at: Optional[datetime] = None
    author_id: str
    author_role: str

# --- Message Schemas ---

class MessageCreate(BaseModel):
    sender_id: str
    receiver_id: str
    content: str
    conversation_id: Optional[str] = None

class Message(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    content: str
    timestamp: datetime
    conversation_id: str

# --- Alert Schemas ---

class AlertCreate(BaseModel):
    user_id: str
    type: str  # "ATTENDANCE", "ASSIGNMENT", "RESULT", "GENERAL"
    title: str
    message: str
    priority: str  # "LOW", "MEDIUM", "HIGH"

class Alert(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    message: str
    priority: str
    is_read: bool = False
    created_at: datetime

# --- Support Case Schemas ---

class SupportCaseCreate(BaseModel):
    student_id: str
    subject: str
    description: str
    assigned_staff_id: Optional[str] = None

class SupportCasePatch(BaseModel):
    status: Optional[str] = None
    assigned_staff_id: Optional[str] = None
    notes: Optional[str] = None

class SupportCase(BaseModel):
    id: str
    student_id: str
    subject: str
    description: str
    status: str  # "OPEN", "IN_PROGRESS", "CLOSED"
    assigned_staff_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
