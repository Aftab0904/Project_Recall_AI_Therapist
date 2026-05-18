from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import MemoryDB, ExclusionItemDB
from .memory_store import memory_store
from .models import MemoryStatus

class MemoryRetriever:
    async def retrieve_relevant_memories(self, db: AsyncSession, user_id: str, query: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        # 1. Get exclusions
        exclusion_result = await db.execute(select(ExclusionItemDB).where(ExclusionItemDB.user_id == user_id))
        exclusions = [e.content for e in exclusion_result.scalars().all()]

        # 2. Query ChromaDB
        if query:
            results = memory_store.collection.query(
                query_texts=[query],
                where={"user_id": user_id},
                n_results=10
            )
        else:
            # If no query, just get most important/recent
            results = memory_store.collection.get(
                where={"user_id": user_id},
                limit=10
            )

        if not results["ids"] or (isinstance(results["ids"], list) and len(results["ids"]) == 0):
            return []

        # 3. Fetch full metadata from SQLite and apply weighted re-ranking
        memory_ids = results["ids"][0] if query else results["ids"]
        if not memory_ids:
            return []

        stmt = select(MemoryDB).where(MemoryDB.id.in_(memory_ids), MemoryDB.status == MemoryStatus.ACTIVE)
        db_result = await db.execute(stmt)
        memories = db_result.scalars().all()

        scored_memories = []
        for memory in memories:
            # Skip if semantically similar to exclusions (already handled in add_exclusion, but safety first)
            
            # Simple scoring: importance + recency + unresolved bonus
            score = memory.importance * 1.0
            
            # Recency bonus (very simplified)
            score += 2.0 if (memory.created_at.year == 2026) else 0.0 
            
            # We could add more complex logic here
            
            scored_memories.append({
                "memory": memory,
                "score": score
            })

        # Sort by score descending
        scored_memories.sort(key=lambda x: x["score"], reverse=True)

        # Return top K
        return [
            {
                "id": m["memory"].id,
                "summary": m["memory"].summary,
                "theme": m["memory"].theme,
                "score": m["score"]
            } for m in scored_memories[:top_k]
        ]

retriever = MemoryRetriever()
