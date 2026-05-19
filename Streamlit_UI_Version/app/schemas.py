from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MemoryType(str, Enum):
    CORE_PROFILE = "core_profile"
    SESSION_EPHEMERAL = "session_ephemeral"
    SAFETY_SIGNAL = "safety_signal"
    STRESS_TRIGGER = "stress_trigger"
    ONGOING_THEME = "ongoing_theme"
    PERSONAL_GOAL = "personal_goal"
    COPING_STRATEGY = "coping_strategy"

class Session(BaseModel):
    session_id: str
    user_id: str
    timestamp: datetime
    theme: str
    emotional_tone: str
    key_moments: List[str]
    closing_state: str
    crisis_signal: bool = False

class Memory(BaseModel):
    memory_id: str
    user_id: str
    memory_type: MemoryType
    summary: str
    emotional_tone: str
    importance: int = Field(ge=1, le=10)
    stability: str # recurring, one_time
    sensitivity: str # low, medium, high
    actionability: str # low, medium, high
    open_loop: bool
    follow_up_suggestion: Optional[str] = None
    do_not_use_for_push: bool = False
    created_at: datetime
    updated_at: datetime
    fingerprint: str

class OpenerResponse(BaseModel):
    message: str
    retrieved_memories: List[Dict[str, Any]]
    source: str # api, fallback
    latency_ms: float

class ChatResponse(BaseModel):
    message: str
    retrieved_memories: List[Dict[str, Any]]
    source: str # api, fallback
    latency_ms: float

class EvaluationResult(BaseModel):
    warmth_score: float
    specificity_score: float
    non_robotic_score: float
    safety_score: float
    length_score: float
    memory_relevance_score: float
    overall_score: float
    notes: List[str]
    latency_ms: float

class SimpleEvaluation(BaseModel):
    memory_coverage: float
    retrieval_recall: float
    human_recall_score: float
    safety_pass: bool
    total_latency_ms: float
