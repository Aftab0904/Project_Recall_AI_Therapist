import re
import time
from typing import List, Dict, Any
from .schemas import Memory

class MemoryRetriever:
    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        return re.findall(r'\w+', text.lower())

    def score_memory(self, query: str, memory: Memory) -> Dict[str, Any]:
        query_tokens = set(self.tokenize(query))
        summary_tokens = set(self.tokenize(memory.summary))
        theme_tokens = set(self.tokenize(memory.summary)) # theme can be part of summary or separate, here we use summary
        
        # Keyword overlap
        overlap = len(query_tokens.intersection(summary_tokens))
        keyword_score = min(overlap / max(len(query_tokens), 1), 1.0) * 10.0
        
        # Importance component
        importance_score = memory.importance * 0.5
        
        # Recency (simplified)
        now_sec = time.time()
        updated_sec = memory.updated_at.timestamp()
        days_diff = (now_sec - updated_sec) / 86400
        recency_score = max(5 - days_diff, 0)
        
        # Open loop bonus
        open_loop_bonus = 2.0 if memory.open_loop else 0.0
        
        # Actionability
        action_map = {"high": 2.0, "medium": 1.0, "low": 0.0}
        action_score = action_map.get(memory.actionability, 0.0)
        
        # Sensitivity penalty (don't retrieve high sensitivity for general chat)
        sensitivity_penalty = 0.0
        if memory.sensitivity == "high":
            sensitivity_penalty = -5.0
            
        final_score = keyword_score + importance_score + recency_score + open_loop_bonus + action_score + sensitivity_penalty
        
        return {
            "score": round(final_score, 2),
            "components": {
                "keyword_overlap": round(keyword_score, 2),
                "importance": importance_score,
                "recency": round(recency_score, 2),
                "open_loop": open_loop_bonus,
                "actionability": action_score,
                "sensitivity_penalty": sensitivity_penalty
            },
            "matched_terms": list(query_tokens.intersection(summary_tokens))
        }

    def retrieve_memories(self, query: str, memories: List[Memory], limit: int = 3) -> List[Dict[str, Any]]:
        scored = []
        for m in memories:
            score_data = self.score_memory(query, m)
            scored.append({
                "memory": m,
                **score_data
            })
        
        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)
        
        # Filter out very low scores or absolute negatives if needed
        results = scored[:limit]
        
        return [
            {
                "memory_id": r["memory"].memory_id,
                "summary": r["memory"].summary,
                "theme": r["memory"].summary.split('.')[0], # proxy for theme
                "score": r["score"],
                "explanation": r["components"],
                "matched_terms": r["matched_terms"]
            } for r in results
        ]

retriever = MemoryRetriever()
