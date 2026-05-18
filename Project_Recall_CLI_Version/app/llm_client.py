import os
import requests
import json
from .utils import get_env_var

class LLMClient:
    def __init__(self):
        self.api_key = get_env_var("OPENROUTER_API_KEY")
        self.base_url = get_env_var("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = get_env_var("MODEL_NAME", "deepseek/deepseek-r1:free")
        self.mock_mode = get_env_var("MOCK_LLM", "false").lower() == "true"

    def chat(self, prompt: str) -> str:
        if self.mock_mode:
            return self._mock_response(prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        if "Extract safe, useful long-term memories" in prompt:
            # Detect theme from prompt to give better mock response
            if "Work anxiety" in prompt:
                return json.dumps([{
                    "memory_type": "stress_trigger",
                    "summary": "Feeling overwhelmed by weekly team meetings and public speaking.",
                    "emotional_tone": "anxious",
                    "importance": 4,
                    "stability": "recurring",
                    "sensitivity": "low",
                    "actionability": "medium",
                    "open_loop": True,
                    "follow_up_suggestion": "Check in on the team meeting feeling.",
                    "do_not_use_for_push": False
                }])
            elif "Conflict with sister" in prompt:
                return json.dumps([{
                    "memory_type": "relationship_context",
                    "summary": "Struggling with boundaries with sister, especially regarding borrowed items.",
                    "emotional_tone": "frustrated",
                    "importance": 3,
                    "stability": "recurring",
                    "sensitivity": "medium",
                    "actionability": "high",
                    "open_loop": False,
                    "follow_up_suggestion": "Ask if the boundary conversation happened.",
                    "do_not_use_for_push": False
                }])
            elif "Sleep issues" in prompt:
                return json.dumps([{
                    "memory_type": "stress_trigger",
                    "summary": "Difficulty sleeping after late-night rumination about work mistakes.",
                    "emotional_tone": "tired",
                    "importance": 5,
                    "stability": "recurring",
                    "sensitivity": "medium",
                    "actionability": "high",
                    "open_loop": True,
                    "follow_up_suggestion": "Check in on sleep quality.",
                    "do_not_use_for_push": False
                }])
            elif "journaling" in prompt:
                return json.dumps([{
                    "memory_type": "positive_progress",
                    "summary": "Started a gratitude journal which helped improve mood in the morning.",
                    "emotional_tone": "hopeful",
                    "importance": 3,
                    "stability": "recurring",
                    "sensitivity": "low",
                    "actionability": "low",
                    "open_loop": False,
                    "follow_up_suggestion": "Acknowledge the progress with journaling.",
                    "do_not_use_for_push": False
                }])
            elif "conversation with manager" in prompt:
                return json.dumps([{
                    "memory_type": "open_loop",
                    "summary": "Planned a difficult conversation with manager about a raise next Tuesday.",
                    "emotional_tone": "determined",
                    "importance": 5,
                    "stability": "one_time",
                    "sensitivity": "low",
                    "actionability": "high",
                    "open_loop": True,
                    "follow_up_suggestion": "Ask how the conversation with the manager went.",
                    "do_not_use_for_push": False
                }])
            
            return json.dumps([{
                "memory_type": "ongoing_theme",
                "summary": "User is working on self-care and setting boundaries.",
                "emotional_tone": "neutral",
                "importance": 3,
                "stability": "unknown",
                "sensitivity": "low",
                "actionability": "medium",
                "open_loop": False,
                "follow_up_suggestion": None,
                "do_not_use_for_push": False
            }])
        
        if "Generate the first message" in prompt:
            return "Welcome back. Last time, that team meeting seemed to be taking up a lot of space. I’m curious how the week has felt since then — especially whether the grounding exercise helped at all."

        return "I'm here to support you. How can I help today?"
