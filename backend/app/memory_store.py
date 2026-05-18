import uuid
from datetime import datetime
from typing import List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .db import MemoryDB, ExclusionItemDB
from .models import MemoryRecord, MemoryStatus, MemoryType, SensitivityLevel
from .config import settings

class MemoryStore:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.collection = self.chroma_client.get_or_create_collection(name="mentra_memories")

    async def add_memory(self, db: AsyncSession, user_id: str, memory_data: dict):
        memory_id = str(uuid.uuid4())
        
        # Add to SQLite
        new_memory = MemoryDB(
            id=memory_id,
            user_id=user_id,
            source_session_id=memory_data.get("source_session_id"),
            memory_type=memory_data["memory_type"],
            theme=memory_data["theme"],
            summary=memory_data["summary"],
            emotional_tone=memory_data["emotional_tone"],
            importance=memory_data["importance"],
            sensitivity=memory_data["sensitivity"],
            safe_to_reference=memory_data["is_safe_to_reference"],
            created_at=datetime.utcnow(),
            status=MemoryStatus.ACTIVE
        )
        db.add(new_memory)
        await db.commit()

        # Add to Chroma if safe to reference
        if memory_data["is_safe_to_reference"]:
            self.collection.add(
                documents=[memory_data["summary"]],
                metadatas=[{
                    "user_id": user_id,
                    "memory_id": memory_id,
                    "theme": memory_data["theme"],
                    "importance": memory_data["importance"],
                    "memory_type": memory_data["memory_type"].value
                }],
                ids=[memory_id]
            )
        
        return memory_id

    async def get_user_memories(self, db: AsyncSession, user_id: str) -> List[MemoryDB]:
        result = await db.execute(
            select(MemoryDB).where(
                MemoryDB.user_id == user_id,
                MemoryDB.status != MemoryStatus.DELETED
            )
        )
        return result.scalars().all()

    async def soft_delete_memory(self, db: AsyncSession, memory_id: str):
        await db.execute(
            update(MemoryDB)
            .where(MemoryDB.id == memory_id)
            .values(status=MemoryStatus.DELETED, deleted_at=datetime.utcnow())
        )
        await db.commit()
        
        # Remove from Chroma
        try:
            self.collection.delete(ids=[memory_id])
        except Exception:
            pass

    async def add_exclusion(self, db: AsyncSession, user_id: str, content: str):
        new_exclusion = ExclusionItemDB(user_id=user_id, content=content)
        db.add(new_exclusion)
        await db.commit()
        
        # Optionally search and delete semantically similar memories
        results = self.collection.query(
            query_texts=[content],
            where={"user_id": user_id},
            n_results=5
        )
        if results["ids"] and results["distances"]:
            for i, distance in enumerate(results["distances"][0]):
                if distance < 0.5: # Threshold for high similarity
                    await self.soft_delete_memory(db, results["ids"][0][i])

memory_store = MemoryStore()
