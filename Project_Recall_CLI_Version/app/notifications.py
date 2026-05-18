from typing import List, Optional, Dict
from .schemas import Session, Memory

class NotificationEngine:
    def get_example_scenarios(self) -> List[Dict]:
        return [
            {
                "scenario": "Unresolved work anxiety",
                "signals": "High stress trigger, open loop, importance 4/5",
                "decision": "Send re-engagement",
                "copy": "That team meeting was weighing on you last time. If you want, we can check in on how it felt and what you need next.",
                "why_safe": "Non-judgmental, references specific work context without medicalizing."
            },
            {
                "scenario": "Positive progress from journaling",
                "signals": "Positive progress type, actionability high",
                "decision": "Send encouragement",
                "copy": "I've been thinking about your progress with journaling. How has your morning mood been feeling lately?",
                "why_safe": "Positive reinforcement, low sensitivity topic."
            },
            {
                "scenario": "Overwhelmed close",
                "signals": "Closing state was 'tired/overwhelmed', unresolved theme",
                "decision": "Send soft check-in",
                "copy": "You mentioned feeling quite drained last time we spoke. I'm curious if you've found any small moments for yourself this week.",
                "why_safe": "Validates user's stated feeling, offers a gentle inquiry."
            }
        ]

    def choose_notification(self, user_settings: Dict, sessions: List[Session], memories: List[Memory]) -> Optional[str]:
        # Safety gates
        if not user_settings.get("opted_in", True):
            return None
            
        # Crisis signal gate
        if any(s.crisis_signal for s in sessions):
            return None
            
        # Notification fatigue gate (mocked)
        if user_settings.get("notifications_last_7_days", 0) >= 2:
            return None
            
        # Choose a memory that is safe for push
        eligible_memories = [
            m for m in memories 
            if m.sensitivity != "high" 
            and not m.do_not_use_for_push
        ]
        
        if not eligible_memories:
            return None
            
        # Return a simple mock copy for the first eligible memory
        return f"Thinking about what you said regarding {eligible_memories[0].summary}. How is that feeling today?"
