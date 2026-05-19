import os
import requests
import json
import time
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-pro-1.5-exp")
        self.mock_mode = os.getenv("MOCK_LLM", "true").lower() == "true"

    def get_status(self) -> Dict[str, Any]:
        return {
            "provider": "Mock LLM" if self.mock_mode else "OpenRouter",
            "model": "deterministic-mock" if self.mock_mode else self.model,
            "api_key_detected": bool(self.api_key),
            "mock_mode": self.mock_mode
        }

    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.4) -> Dict[str, Any]:
        if self.mock_mode or not self.api_key:
            return {"content": None, "source": "fallback", "latency_ms": 0}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Project Recall Streamlit"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1000
        }

        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return {
                    "content": content,
                    "source": "api",
                    "latency_ms": latency
                }
            else:
                return {
                    "content": None,
                    "source": "fallback",
                    "latency_ms": latency,
                    "error": f"API Error: {response.status_code}"
                }
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {
                "content": None,
                "source": "fallback",
                "latency_ms": latency,
                "error": str(e)
            }

llm_client = LLMClient()
