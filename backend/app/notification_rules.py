from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import MemoryDB, SessionDB, NotificationEventDB
from .models import MemoryStatus, MemoryType

class NotificationEngine:
    async def evaluate_triggers(self, db: AsyncSession, user_id: str) -> dict:
        # 1. Check for notification cooldown (e.g., max 1 per week)
        last_event_stmt = select(NotificationEventDB).where(NotificationEventDB.user_id == user_id).order_by(NotificationEventDB.sent_at.desc()).limit(1)
        last_event = (await db.execute(last_event_stmt)).scalars().first()
        
        if last_event and datetime.utcnow() - last_event.sent_at < timedelta(days=7):
            return {"should_send": False, "reason": "cooldown_active"}

        # 2. Get session history
        sessions_stmt = select(SessionDB).where(SessionDB.user_id == user_id).order_by(SessionDB.timestamp.desc()).limit(1)
        last_session = (await db.execute(sessions_stmt)).scalars().first()
        
        if not last_session:
            return {"should_send": False, "reason": "no_session_history"}

        days_away = (datetime.utcnow() - last_session.timestamp).days

        # 3. Get unresolved memories
        memories_stmt = select(MemoryDB).where(
            MemoryDB.user_id == user_id,
            MemoryDB.status == MemoryStatus.ACTIVE,
            MemoryDB.memory_type == MemoryType.SESSION_EPHEMERAL
        )
        unresolved_memories = (await db.execute(memories_stmt)).scalars().all()

        # Logic Scenarios
        
        # Scenario A: Work anxiety after 3+ days
        work_anxiety = [m for m in unresolved_memories if "work" in m.theme.lower() or "anxiety" in m.theme.lower()]
        if days_away >= 3 and work_anxiety:
            return {
                "should_send": True,
                "scenario": "work_anxiety_checkin",
                "reason": f"User has been away for {days_away} days with unresolved work anxiety.",
                "copy": "Hi there. I was thinking about our last talk about work. It seemed like a lot was on your mind. Just wanted to see how you're feeling today."
            }

        # Scenario B: Coping/Homework plan after 2+ days
        coping_plan = [m for m in unresolved_memories if "plan" in m.summary.lower() or "practice" in m.summary.lower()]
        if days_away >= 2 and coping_plan:
            return {
                "should_send": True,
                "scenario": "coping_plan_followup",
                "reason": "User has been away for 2 days after discussing a coping plan.",
                "copy": "Hello. I was wondering if you've had a chance to try that breathing exercise we talked about. No pressure if not, just checking in."
            }

        # Scenario C: Overwhelmed/Sad close after 1+ day
        if days_away >= 1 and last_session.emotional_tone in ["Overwhelmed", "Sad", "Heavy"]:
            return {
                "should_send": True,
                "scenario": "emotional_baseline_check",
                "reason": "User left the last session feeling heavy and has been away for 1 day.",
                "copy": "Hi. Our last session felt a bit heavy toward the end. I'm here if you'd like to share how you're doing today."
            }

        return {"should_send": False, "reason": "no_triggers_matched"}

notification_engine = NotificationEngine()
