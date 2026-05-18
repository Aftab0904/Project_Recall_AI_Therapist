import json
import httpx
import re
from typing import Optional, Dict, Any, List
from .config import settings

class LLMClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.timeout = httpx.Timeout(60.0, connect=10.0)

    async def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        if self.provider == "mock":
            return self._mock_response(prompt)
        
        response_text = ""
        if self.provider == "ollama":
            response_text = await self._ollama_generate(prompt, system_prompt)
        elif self.provider == "openrouter":
            response_text = await self._openrouter_generate(prompt, system_prompt)
        else:
            response_text = self._deterministic_fallback(prompt)
            
        return self.clean_json_response(response_text)

    def clean_json_response(self, text: str) -> str:
        """
        Strips <think> tags, markdown code blocks, and extra whitespace 
        to ensure valid JSON parsing.
        """
        if text is None:
            return ""
            
        # Remove <think>...</think> blocks if present (common in DeepSeek-R1)
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # Strip markdown code blocks (e.g., ```json ... ```)
        text = re.sub(r'```(?:json)?\s*(.*?)\s*```', r'\1', text, flags=re.DOTALL)
        
        # If there's still non-JSON text around the JSON object, try to find the first '{' and last '}'
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
            
        return text.strip()

    async def _ollama_generate(self, prompt: str, system_prompt: str) -> str:
        url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()["message"]["content"]
            except Exception as e:
                print(f"Ollama Error: {e}")
                return self._deterministic_fallback(prompt)

    async def _openrouter_generate(self, prompt: str, system_prompt: str) -> str:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/mentra-ai/project-recall", # Required by some OpenRouter models
            "X-Title": "Mentra Project Recall"
        }
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"OpenRouter Error: {e}")
                return self._deterministic_fallback(prompt)

    def _mock_response(self, prompt: str) -> str:
        # (Rest of mock logic unchanged ...)
        # Simple mock logic based on prompt keywords
        if "extract" in prompt.lower() or "memory" in prompt.lower():
            return json.dumps({
                "memories": [
                    {
                        "summary": "User shared feeling overwhelmed by work boundaries.",
                        "memory_type": "session_ephemeral",
                        "theme": "Work-Life Balance",
                        "emotional_tone": "Anxious",
                        "importance": 7,
                        "sensitivity": "medium",
                        "is_safe_to_reference": True,
                        "unresolved_status_bonus": True
                    }
                ]
            })
        elif "opener" in prompt.lower() or "warm" in prompt.lower():
            return json.dumps({
                "message": "Welcome back. I was thinking about our last talk regarding your work boundaries. How are things feeling in that area today?",
                "memories_used": ["Work-Life Balance"]
            })
        elif "safety" in prompt.lower():
            return json.dumps({"is_safe": True, "risk_level": "low"})
        
        return json.dumps({"message": "I'm here to listen."})

    def _deterministic_fallback(self, prompt: str) -> str:
        # Basic fallback for when APIs fail
        if "extract" in prompt.lower():
            return json.dumps({"memories": []})
        return json.dumps({"message": "Hello. It's good to see you again. How would you like to start today?"})

llm_client = LLMClient()
