from datetime import datetime, timedelta

SAMPLE_SESSIONS = [
    {
        "session_id": "s1",
        "user_id": "demo_user",
        "timestamp": datetime.utcnow() - timedelta(days=10),
        "theme": "Work Anxiety",
        "emotional_tone": "Anxious",
        "raw_transcript": "User mentioned feeling overwhelmed by constant Slack messages and a lack of boundaries with their manager. They find it hard to disconnect after 6 PM.",
        "key_moments": [
            {"timestamp": "10:05", "content": "Manager messaged me at 9 PM again.", "emotion": "Frustrated"}
        ]
    },
    {
        "session_id": "s2",
        "user_id": "demo_user",
        "timestamp": datetime.utcnow() - timedelta(days=8),
        "theme": "Sleep Issues",
        "emotional_tone": "Tired",
        "raw_transcript": "User is having trouble falling asleep because they are ruminating about work emails. They started trying a digital detox after 8 PM.",
        "key_moments": [
            {"timestamp": "05:20", "content": "I lie awake thinking about the inbox.", "emotion": "Exhausted"}
        ]
    },
    {
        "session_id": "s3",
        "user_id": "demo_user",
        "timestamp": datetime.utcnow() - timedelta(days=6),
        "theme": "Family Pressure",
        "emotional_tone": "Guilty",
        "raw_transcript": "User discussed pressure from parents to visit more often. They feel guilty for saying no, even though they are burnt out from work.",
        "key_moments": [
            {"timestamp": "15:45", "content": "My mom said I don't care about the family.", "emotion": "Sad"}
        ]
    },
    {
        "session_id": "s4",
        "user_id": "demo_user",
        "timestamp": datetime.utcnow() - timedelta(days=4),
        "theme": "Boundary Progress",
        "emotional_tone": "Hopeful",
        "raw_transcript": "User successfully told their manager they wouldn't be available after 7 PM. They felt a sense of relief but also slight lingering anxiety.",
        "key_moments": [
            {"timestamp": "08:30", "content": "I finally said no to the late meeting.", "emotion": "Proud"}
        ]
    },
    {
        "session_id": "s5",
        "user_id": "demo_user",
        "timestamp": datetime.utcnow() - timedelta(days=2),
        "theme": "Unresolved Concerns",
        "emotional_tone": "Heavy",
        "raw_transcript": "User closed the session saying they are still worried about the upcoming performance review despite their boundary progress.",
        "key_moments": [
            {"timestamp": "42:00", "content": "What if my boundaries hurt my review?", "emotion": "Worried"}
        ]
    }
]
