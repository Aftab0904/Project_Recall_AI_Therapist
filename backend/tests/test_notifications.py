import pytest
from datetime import datetime, timedelta
from app.notification_rules import notification_engine
from app.db import AsyncSessionLocal, init_db, SessionDB, MemoryDB
from app.models import MemoryType, SensitivityLevel, MemoryStatus

@pytest.mark.asyncio
async def test_notification_triggers():
    await init_db()
    async with AsyncSessionLocal() as db:
        # Setup trigger condition: Away 3 days with work anxiety
        user_id = "notif_test_user"
        
        # Last session 3 days ago
        db.add(SessionDB(
            id="notif_s1",
            user_id=user_id,
            timestamp=datetime.utcnow() - timedelta(days=3),
            theme="Work",
            emotional_tone="Anxious"
        ))
        
        # Active work memory
        db.add(MemoryDB(
            id="notif_m1",
            user_id=user_id,
            memory_type=MemoryType.SESSION_EPHEMERAL,
            theme="Work Anxiety",
            summary="User is worried about deadline",
            emotional_tone="Anxious",
            importance=8,
            sensitivity=SensitivityLevel.LOW,
            safe_to_reference=True,
            status=MemoryStatus.ACTIVE
        ))
        
        await db.commit()
        
        result = await notification_engine.evaluate_triggers(db, user_id)
        assert result["should_send"] is True
        assert result["scenario"] == "work_anxiety_checkin"
