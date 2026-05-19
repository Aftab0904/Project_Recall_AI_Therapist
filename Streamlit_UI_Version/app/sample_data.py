from datetime import datetime
from .schemas import MemoryType

MOCK_MEMORIES = [
    {
        "theme": "Work Anxiety",
        "memory_type": MemoryType.STRESS_TRIGGER,
        "summary": "User feels tense before weekly team meetings and worries their manager may judge their ideas.",
        "emotional_tone": "anxious",
        "importance": 5,
        "stability": "recurring",
        "sensitivity": "medium",
        "actionability": "high",
        "open_loop": True,
        "follow_up_suggestion": "Ask how the next team meeting felt and whether grounding helped.",
        "do_not_use_for_push": False
    },
    {
        "theme": "Work-Life Boundaries",
        "memory_type": MemoryType.ONGOING_THEME,
        "summary": "User feels work messages spill into evenings and wants clearer separation between work and personal time.",
        "emotional_tone": "overwhelmed",
        "importance": 5,
        "stability": "recurring",
        "sensitivity": "medium",
        "actionability": "high",
        "open_loop": True,
        "follow_up_suggestion": "Ask whether they tried a shutdown routine after work.",
        "do_not_use_for_push": False
    },
    {
        "theme": "Sleep Rumination",
        "memory_type": MemoryType.STRESS_TRIGGER,
        "summary": "User wakes around 4 AM and replays work conversations, especially after late-night phone use.",
        "emotional_tone": "tired",
        "importance": 4,
        "stability": "recurring",
        "sensitivity": "medium",
        "actionability": "high",
        "open_loop": False,
        "follow_up_suggestion": "Ask whether a wind-down routine helped.",
        "do_not_use_for_push": False
    },
    {
        "theme": "Family Boundary Goal",
        "memory_type": MemoryType.PERSONAL_GOAL,
        "summary": "User wants to set a calmer boundary with their sister without feeling selfish.",
        "emotional_tone": "conflicted",
        "importance": 4,
        "stability": "one_time",
        "sensitivity": "medium",
        "actionability": "medium",
        "open_loop": True,
        "follow_up_suggestion": "Ask whether they used the sentence they drafted.",
        "do_not_use_for_push": True
    },
    {
        "theme": "Morning Walks",
        "memory_type": MemoryType.COPING_STRATEGY,
        "summary": "User feels better after morning walks and wants to continue small routines.",
        "emotional_tone": "hopeful",
        "importance": 3,
        "stability": "recurring",
        "sensitivity": "low",
        "actionability": "high",
        "open_loop": False,
        "follow_up_suggestion": "Encourage small routines rather than big changes.",
        "do_not_use_for_push": False
    },
    {
        "theme": "Journaling Helps",
        "memory_type": MemoryType.COPING_STRATEGY,
        "summary": "User said journaling helped organize their thoughts and made the week feel more manageable.",
        "emotional_tone": "hopeful",
        "importance": 3,
        "stability": "recurring",
        "sensitivity": "low",
        "actionability": "high",
        "open_loop": False,
        "follow_up_suggestion": "Ask whether journaling still feels useful.",
        "do_not_use_for_push": False
    }
]

EXPECTED_MEMORIES_COUNT = 6
