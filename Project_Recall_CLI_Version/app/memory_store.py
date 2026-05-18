import json
import os
from typing import List
from .schemas import Memory, MemoryStoreData

class MemoryStore:
    def __init__(self, file_path: str = "outputs/memory_store.json"):
        self.file_path = file_path
        self.data = self._load()

    def _load(self) -> MemoryStoreData:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    content = json.load(f)
                    return MemoryStoreData(**content)
            except (json.JSONDecodeError, ValueError):
                return MemoryStoreData()
        return MemoryStoreData()

    def save(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as f:
            f.write(self.data.model_dump_json(indent=2))

    def add_memories(self, memories: List[Memory]):
        self.data.memories.extend(memories)
        self.save()

    def get_user_memories(self, user_id: str) -> List[Memory]:
        return [m for m in self.data.memories if m.user_id == user_id]

    def clear(self):
        self.data = MemoryStoreData()
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
