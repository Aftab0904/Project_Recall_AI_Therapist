import json
from datetime import datetime
from typing import List
from .schemas import Session, Memory
from .llm_client import LLMClient
from .prompts import MEMORY_EXTRACTION_PROMPT
from .utils import generate_id

class MemoryExtractor:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def extract_memories(self, session: Session) -> List[Memory]:
        prompt = MEMORY_EXTRACTION_PROMPT.format(
            theme=session.theme,
            emotional_tone=session.emotional_tone,
            key_moments=", ".join(session.key_moments),
            closing_state=session.closing_state,
            data=session.model_dump_json()
        )
        
        response = self.llm_client.chat(prompt)
        
        try:
            # Clean response if it contains markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            memories_data = json.loads(response)
            if not isinstance(memories_data, list):
                memories_data = [memories_data]
                
            memories = []
            for m in memories_data:
                memory = Memory(
                    memory_id=generate_id("mem_"),
                    user_id=session.user_id,
                    source_session_id=session.session_id,
                    created_at=datetime.now(),
                    **m
                )
                memories.append(memory)
            return memories
        except Exception as e:
            print(f"Error parsing memories: {e}")
            return []
