import json
from typing import List, Dict, Any, TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, END
from .llm_client import llm_client
from .safety import safety_engine
from .memory_store import memory_store
from .retriever import retriever
from .db import AsyncSessionLocal
from .models import MemoryType, SensitivityLevel

class GraphState(TypedDict):
    user_id: str
    session_id: Optional[str]
    raw_transcript: Optional[str]
    current_message: Optional[str]
    extracted_memories: List[Dict[str, Any]]
    retrieved_memories: List[Dict[str, Any]]
    is_safe: bool
    safety_notes: str
    generated_opener: str
    memories_used: List[str]

async def validate_and_prepare(state: GraphState) -> GraphState:
    # Basic validation
    state["is_safe"] = True
    return state

async def extract_memories(state: GraphState) -> GraphState:
    if not state.get("raw_transcript"):
        return state

    prompt = f"""
    Extract key structured memories from this therapy session transcript.
    Focus on:
    - Recurring struggles
    - Coping styles
    - Life context
    - Unresolved themes
    
    Transcript: {state["raw_transcript"]}
    
    Return a JSON object with a 'memories' list:
    {{
        "memories": [
            {{
                "summary": "Concise summary",
                "memory_type": "core_profile" | "session_ephemeral",
                "theme": "Broad theme",
                "emotional_tone": "Tone",
                "importance": 1-10,
                "sensitivity": "low" | "medium" | "high",
                "is_safe_to_reference": bool
            }}
        ]
    }}
    """
    system_prompt = "You are a specialized clinical memory extractor. Extract objective, safe, and helpful memories without clinical diagnosis."
    
    response = await llm_client.generate_response(prompt, system_prompt)
    try:
        data = json.loads(response)
        state["extracted_memories"] = data.get("memories", [])
    except:
        state["extracted_memories"] = []
    
    return state

async def safety_filter(state: GraphState) -> GraphState:
    # Filter extracted memories for safety
    safe_memories = []
    for m in state.get("extracted_memories", []):
        safety_check = await safety_engine.analyze_safety(m["summary"])
        if safety_check.get("is_safe", True):
            safe_memories.append(m)
        else:
            state["is_safe"] = False
            state["safety_notes"] = "Some content was flagged as unsafe and excluded."
    
    state["extracted_memories"] = safe_memories
    return state

async def persist_memories(state: GraphState) -> GraphState:
    async with AsyncSessionLocal() as db:
        for m in state.get("extracted_memories", []):
            m["source_session_id"] = state.get("session_id")
            # Convert string to enum
            m["memory_type"] = MemoryType(m["memory_type"])
            m["sensitivity"] = SensitivityLevel(m["sensitivity"])
            await memory_store.add_memory(db, state["user_id"], m)
    return state

async def retrieve_memories(state: GraphState) -> GraphState:
    async with AsyncSessionLocal() as db:
        memories = await retriever.retrieve_relevant_memories(
            db, state["user_id"], state.get("current_message")
        )
        state["retrieved_memories"] = memories
    return state

async def generate_opener(state: GraphState) -> GraphState:
    memories_str = "\n".join([f"- {m['summary']} (Theme: {m['theme']})" for m in state["retrieved_memories"]])
    
    prompt = f"""
    Generate a warm, human, non-robotic session-opening message for a returning user.
    Reference one relevant past topic gently. Do NOT list facts. 
    Ask permission to continue or offer to talk about something new.
    
    Past Context:
    {memories_str}
    
    User's current message (if any): {state.get("current_message", "None")}
    
    Return a JSON object:
    {{
        "message": "Warm message here",
        "memories_used": ["Theme names"]
    }}
    """
    system_prompt = "You are Mentra, a warm and empathetic AI therapist. You remember what matters but you aren't creepy or robotic about it."
    
    response = await llm_client.generate_response(prompt, system_prompt)
    try:
        data = json.loads(response)
        state["generated_opener"] = data["message"]
        state["memories_used"] = data["memories_used"]
    except:
        state["generated_opener"] = "Welcome back. I'm glad to see you again. How would you like to start today?"
        state["memories_used"] = []
    
    return state

# Ingestion Flow
ingest_builder = StateGraph(GraphState)
ingest_builder.add_node("validate", validate_and_prepare)
ingest_builder.add_node("extract", extract_memories)
ingest_builder.add_node("filter", safety_filter)
ingest_builder.add_node("persist", persist_memories)

ingest_builder.set_entry_point("validate")
ingest_builder.add_edge("validate", "extract")
ingest_builder.add_edge("extract", "filter")
ingest_builder.add_edge("filter", "persist")
ingest_builder.add_edge("persist", END)

ingest_flow = ingest_builder.compile()

# Opener Flow
opener_builder = StateGraph(GraphState)
opener_builder.add_node("retrieve", retrieve_memories)
opener_builder.add_node("generate", generate_opener)

opener_builder.set_entry_point("retrieve")
opener_builder.add_edge("retrieve", "generate")
opener_builder.add_edge("generate", END)

opener_flow = opener_builder.compile()
