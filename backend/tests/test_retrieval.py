import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.retriever import retriever
from app.db import AsyncSessionLocal, init_db
from app.memory_store import memory_store
from app.models import MemoryType, SensitivityLevel

@pytest.mark.asyncio
async def test_retrieval_logic():
    await init_db()
    async with AsyncSessionLocal() as db:
        # Add a test memory
        await memory_store.add_memory(db, "test_user", {
            "summary": "Test work memory",
            "memory_type": MemoryType.SESSION_EPHEMERAL,
            "theme": "Work",
            "emotional_tone": "Neutral",
            "importance": 5,
            "sensitivity": SensitivityLevel.LOW,
            "is_safe_to_reference": True
        })
        
        memories = await retriever.retrieve_relevant_memories(db, "test_user", "work stress")
        assert len(memories) > 0
        assert "Test work memory" in memories[0]["summary"]
