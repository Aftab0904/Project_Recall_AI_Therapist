import os
import shutil
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from .db import init_db, get_db, SessionDB, MemoryDB, ExclusionItemDB, NotificationEventDB, engine
from .models import (
    IngestResponse, OpeningMessageRequest, OpeningMessageResponse,
    NotificationTriggerResponse, ForgetMemoryRequest, MemoryRecord,
    MemoryStatus
)
from .memory_graph import ingest_flow, opener_flow
from .sample_data import SAMPLE_SESSIONS
from .memory_store import memory_store
from .notification_rules import notification_engine
from .config import settings

app = FastAPI(title="Mentra Project Recall API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health")
async def health():
    return {"status": "healthy", "provider": settings.LLM_PROVIDER}

@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_samples(db: AsyncSession = Depends(get_db)):
    print("Starting ingestion of sample sessions...")
    memories_count = 0
    summaries = []
    
    for i, session_data in enumerate(SAMPLE_SESSIONS):
        # Check if session already exists
        existing_session = await db.execute(select(SessionDB).where(SessionDB.id == session_data["session_id"]))
        if existing_session.scalars().first():
            print(f"Session {session_data['session_id']} already exists, skipping DB insert...")
        else:
            print(f"Processing session {i+1}/{len(SAMPLE_SESSIONS)}: {session_data['theme']}...")
            # Save session to DB
            session_db = SessionDB(
                id=session_data["session_id"],
                user_id=session_data["user_id"],
                timestamp=session_data["timestamp"],
                theme=session_data["theme"],
                emotional_tone=session_data["emotional_tone"],
                raw_transcript=session_data["raw_transcript"]
            )
            db.add(session_db)
        
        # Run LangGraph ingest flow (we run this even if session exists to ensure memories are extracted)
        state = {
            "user_id": session_data["user_id"],
            "session_id": session_data["session_id"],
            "raw_transcript": session_data["raw_transcript"],
            "current_message": None,
            "extracted_memories": [],
            "retrieved_memories": [],
            "is_safe": True,
            "safety_notes": "",
            "generated_opener": "",
            "memories_used": []
        }
        final_state = await ingest_flow.ainvoke(state)
        
        memories_count += len(final_state.get("extracted_memories", []))
        for m in final_state.get("extracted_memories", []):
            summaries.append(m["summary"])
            
    await db.commit()
    return {
        "session_count": len(SAMPLE_SESSIONS),
        "memories_extracted": memories_count,
        "summary": summaries
    }

@app.post("/api/session/start", response_model=OpeningMessageResponse)
async def start_session(req: OpeningMessageRequest, db: AsyncSession = Depends(get_db)):
    state = {
        "user_id": req.user_id,
        "session_id": None,
        "raw_transcript": None,
        "current_message": req.current_message,
        "extracted_memories": [],
        "retrieved_memories": [],
        "is_safe": True,
        "safety_notes": "",
        "generated_opener": "",
        "memories_used": []
    }
    
    final_state = await opener_flow.ainvoke(state)
    
    return {
        "message": final_state["generated_opener"],
        "memories_used": final_state["memories_used"],
        "safety_notes": final_state.get("safety_notes")
    }

@app.get("/api/memories/{user_id}", response_model=List[MemoryRecord])
async def get_memories(user_id: str, db: AsyncSession = Depends(get_db)):
    memories = await memory_store.get_user_memories(db, user_id)
    # Convert DB models to Pydantic records
    return [
        MemoryRecord(
            id=m.id,
            user_id=m.user_id,
            source_session_id=m.source_session_id,
            memory_type=m.memory_type,
            theme=m.theme,
            summary=m.summary,
            emotional_tone=m.emotional_tone,
            status=m.status,
            importance=m.importance,
            sensitivity=m.sensitivity,
            safe_to_reference=m.safe_to_reference,
            created_at=m.created_at,
            last_mentioned_at=m.last_mentioned_at,
            deleted_at=m.deleted_at
        ) for m in memories
    ]

@app.delete("/api/memories/{memory_id}")
async def delete_memory(memory_id: str, db: AsyncSession = Depends(get_db)):
    await memory_store.soft_delete_memory(db, memory_id)
    return {"status": "deleted"}

@app.post("/api/memories/exclude")
async def exclude_memory(req: ForgetMemoryRequest, db: AsyncSession = Depends(get_db)):
    if req.memory_id:
        await memory_store.soft_delete_memory(db, req.memory_id)
    if req.content_to_exclude:
        await memory_store.add_exclusion(db, req.user_id, req.content_to_exclude)
    return {"status": "excluded"}

@app.post("/api/notifications/trigger", response_model=NotificationTriggerResponse)
async def trigger_notification(req: OpeningMessageRequest, db: AsyncSession = Depends(get_db)):
    result = await notification_engine.evaluate_triggers(db, req.user_id)
    
    if result["should_send"]:
        # Log the event
        event = NotificationEventDB(
            user_id=req.user_id,
            scenario=result["scenario"],
            copy_sent=result["copy"]
        )
        db.add(event)
        await db.commit()
        
    return NotificationTriggerResponse(
        should_send=result["should_send"],
        scenario=result.get("scenario"),
        reason=result.get("reason"),
        copy=result.get("copy")
    )

@app.post("/api/demo/reset")
async def reset_demo():
    # Dispose of the engine to release the file lock on Windows
    await engine.dispose()
    
    # Delete SQLite DB
    db_path = "./mentra_memory.db"
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception as e:
            print(f"Error removing DB: {e}")
    
    # Delete Chroma DB
    if os.path.exists(settings.CHROMA_PERSIST_DIR):
        try:
            shutil.rmtree(settings.CHROMA_PERSIST_DIR)
        except Exception as e:
            print(f"Error removing Chroma: {e}")
    
    # Re-init
    await init_db()
    return {"status": "reset_complete"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
