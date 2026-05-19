from typing import List, Dict, Any

class NotificationEngine:
    def get_notification_scenarios(self, memories: List[Any]) -> List[Dict[str, Any]]:
        scenarios = [
            {
                "id": 1,
                "name": "Unresolved work anxiety after 3 days",
                "signals": ["Work-Life balance", "anxiety", "3 days since session"],
                "decision": "Send notification",
                "copy": "That team meeting was weighing on you last time. If you want, we can check in on how it felt and what you need next.",
                "safety_rationale": "Uses low-pressure inquiry, avoids mentioning specific sensitive details, focuses on check-in rather than fix."
            },
            {
                "id": 2,
                "name": "Positive journaling progress after 5 days",
                "signals": ["Journaling", "hopeful", "5 days since session"],
                "decision": "Send notification",
                "copy": "You mentioned journaling helped organize your thoughts last week. Want to build on that today?",
                "safety_rationale": "Reinforces positive coping strategies, stays under the frequency cap, assumes a supportive role."
            },
            {
                "id": 3,
                "name": "Overwhelmed close after 4 days",
                "signals": ["Overwhelmed", "4 days since session", "Boundary goal"],
                "decision": "Send notification",
                "copy": "If today feels like a lot, we can start small and pick up from where things felt most tangled.",
                "safety_rationale": "Acknowledges previous state gently, offers a low-barrier starting point, maintains care continuity."
            }
        ]
        return scenarios

notification_engine = NotificationEngine()
