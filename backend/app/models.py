from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class MemoryType(str, Enum):
    CORE_PROFILE = "core_profile"
    SESSION_EPHEMERAL = "session_ephemeral"
    SAFETY_SIGNAL = "safety_signal"

class SensitivityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MemoryStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    DELETED = "deleted"
    ARCHIVED = "archived"

class KeyMoment(BaseModel):
    timestamp: str
    content: str
    emotion: str

class SessionTranscript(BaseModel):
    session_id: str
    user_id: str
    timestamp: datetime
    theme: str
    emotional_tone: str
    key_moments: List[KeyMoment]
    raw_text: Optional[str] = None

class ExtractedMemory(BaseModel):
    summary: str
    memory_type: MemoryType
    theme: str
    emotional_tone: str
    importance: int = Field(ge=1, le=10)
    sensitivity: SensitivityLevel
    is_safe_to_reference: bool
    unresolved_status_bonus: bool = False

class MemoryRecord(BaseModel):
    id: str
    user_id: str
    source_session_id: Optional[str] = None
    memory_type: MemoryType
    theme: str
    summary: str
    emotional_tone: str
    status: MemoryStatus = MemoryStatus.ACTIVE
    importance: int
    sensitivity: SensitivityLevel
    safe_to_reference: bool
    created_at: datetime
    last_mentioned_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class OpeningMessageRequest(BaseModel):
    user_id: str
    current_message: Optional[str] = None

class OpeningMessageResponse(BaseModel):
    message: str
    memories_used: List[str]
    safety_notes: Optional[str] = None

class NotificationTriggerRequest(BaseModel):
    user_id: str

class NotificationTriggerResponse(BaseModel):
    should_send: bool
    scenario: Optional[str] = None
    reason: Optional[str] = None
    message_copy: Optional[str] = Field(None, alias="copy")

class ForgetMemoryRequest(BaseModel):
    user_id: str
    memory_id: Optional[str] = None
    content_to_exclude: Optional[str] = None

class IngestResponse(BaseModel):
    session_count: int
    memories_extracted: int
    summary: List[str]
