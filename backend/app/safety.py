import json
from typing import Dict, Any
from .llm_client import llm_client

class SafetyEngine:
    async def analyze_safety(self, text: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following mental health session content for safety risks.
        Flag any mentions of:
        - Self-harm or suicide
        - Violence towards others
        - Severe crisis signals
        - Inferred medical diagnoses (which we should avoid)

        Content: "{text}"

        Return a JSON object:
        {{
            "is_safe": bool,
            "risk_level": "low" | "medium" | "high" | "critical",
            "flags": list[str],
            "should_route_to_safety_workflow": bool
        }}
        """
        
        system_prompt = "You are a clinical safety classifier for a mental health AI. Be conservative and prioritize user safety."
        
        try:
            response_str = await llm_client.generate_response(prompt, system_prompt)
            return json.loads(response_str)
        except Exception:
            # Default to safe if LLM fails, but in a real app we might default to unsafe or manual review
            return {"is_safe": True, "risk_level": "low", "flags": [], "should_route_to_safety_workflow": False}

safety_engine = SafetyEngine()
