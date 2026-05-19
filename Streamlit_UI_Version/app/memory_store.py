import json
import os
import uuid
from typing import List, Dict, Any
from .schemas import Memory, MemoryType
from .utils import generate_fingerprint, get_current_timestamp

class MemoryStore:
    def __init__(self, file_path: str = "outputs/memory_store.json"):
        self.file_path = file_path
        self._ensure_file_exists()
        self.memories: Dict[str, Memory] = self._load_memories()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def _load_memories(self) -> Dict[str, Memory]:
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return {k: Memory(**v) for k, v in data.items()}
        except Exception:
            return {}

    def _save_memories(self):
        with open(self.file_path, 'w') as f:
            json.dump({k: v.dict() for k, v in self.memories.items()}, f, default=str)

    def add_memory(self, user_id: str, memory_data: Dict[str, Any]) -> str:
        """Add a memory with deduplication using fingerprint."""
        fingerprint = generate_fingerprint(
            user_id, 
            memory_data["memory_type"], 
            memory_data["summary"]
        )
        
        # Check if exists
        existing_id = None
        for mid, m in self.memories.items():
            if m.fingerprint == fingerprint:
                existing_id = mid
                break
        
        now = get_current_timestamp()
        
        if existing_id:
            # Update existing
            self.memories[existing_id].updated_at = now
            self.memories[existing_id].importance = max(self.memories[existing_id].importance, memory_data.get("importance", 1))
            self.memories[existing_id].open_loop = memory_data.get("open_loop", self.memories[existing_id].open_loop)
            self._save_memories()
            return existing_id
        else:
            # Create new
            memory_id = f"mem_{uuid.uuid4().hex[:8]}"
            new_memory = Memory(
                memory_id=memory_id,
                user_id=user_id,
                memory_type=memory_data["memory_type"],
                summary=memory_data["summary"],
                emotional_tone=memory_data["emotional_tone"],
                importance=memory_data["importance"],
                stability=memory_data["stability"],
                sensitivity=memory_data["sensitivity"],
                actionability=memory_data["actionability"],
                open_loop=memory_data["open_loop"],
                follow_up_suggestion=memory_data.get("follow_up_suggestion"),
                do_not_use_for_push=memory_data.get("do_not_use_for_push", False),
                created_at=now,
                updated_at=now,
                fingerprint=fingerprint
            )
            self.memories[memory_id] = new_memory
            self._save_memories()
            return memory_id

    def get_memories(self, user_id: str) -> List[Memory]:
        return [m for m in self.memories.values() if m.user_id == user_id]

    def reset(self):
        self.memories = {}
        self._save_memories()

memory_store = MemoryStore()
