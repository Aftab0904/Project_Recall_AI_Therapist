from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime

class Session(BaseModel):
    session_id: str
    user_id: str
    timestamp: str
    theme: str
    emotional_tone: str
    key_moments: List[str]
    closing_state: str
    crisis_signal: bool = False

class Memory(BaseModel):
    memory_id: str = Field(description="generated string like mem_xxxxxxxx")
    user_id: str
    source_session_id: str
    created_at: datetime
    memory_type: Literal[
        "ongoing_theme",
        "coping_strategy",
        "personal_goal",
        "relationship_context",
        "stress_trigger",
        "positive_progress",
        "open_loop",
        "preference"
    ]
    summary: str
    emotional_tone: str
    importance: int = Field(ge=1, le=5)
    stability: Literal["one_time", "recurring", "unknown"]
    sensitivity: Literal["low", "medium", "high"]
    actionability: Literal["low", "medium", "high"]
    open_loop: bool
    follow_up_suggestion: Optional[str] = None
    do_not_use_for_push: bool = False
    expires_at: Optional[datetime] = None

class MemoryStoreData(BaseModel):
    memories: List[Memory] = []
