from typing import List
from .schemas import Memory

class MemoryRetriever:
    def __init__(self, memories: List[Memory]):
        self.memories = memories

    def get_top_memories(self, user_id: str, limit: int = 3) -> List[Memory]:
        user_memories = [m for m in self.memories if m.user_id == user_id]
        
        # Exclude high sensitivity memories for openers
        safe_memories = [m for m in user_memories if m.sensitivity != "high"]
        
        # Scoring logic requested by user:
        # importance_score = importance / 5
        # open_loop_bonus = 1.0 if open_loop else 0.0
        # actionability_score = {"low": 0.2, "medium": 0.6, "high": 1.0}
        # score = 0.45 * importance_score + 0.30 * open_loop_bonus + 0.25 * actionability_score
        
        action_map = {"low": 0.2, "medium": 0.6, "high": 1.0}
        
        scored_memories = []
        for m in safe_memories:
            importance_score = m.importance / 5.0
            open_loop_bonus = 1.0 if m.open_loop else 0.0
            actionability_score = action_map.get(m.actionability, 0.2)
            
            score = 0.45 * importance_score + 0.30 * open_loop_bonus + 0.25 * actionability_score
            scored_memories.append((score, m))
            
        # Sort by score descending
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        return [m for score, m in scored_memories[:limit]]
