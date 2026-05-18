MEMORY_EXTRACTION_PROMPT = """
You are an expert AI therapist. Extract safe, useful long-term memories from the following session data.

Session Theme: {theme}
Emotional Tone: {emotional_tone}
Key Moments: {key_moments}
Closing State: {closing_state}

Instructions:
- Extract safe, useful long-term memories from a mental-health support session.
- Return ONLY valid JSON as a list of memory objects.
- Do not infer diagnoses.
- Do not store raw quotes unless necessary.
- Do not store highly sensitive details unless essential for continuity.
- Do not include third-party identifying details.
- Mark memories that should not be used for push notifications (do_not_use_for_push).
- Use the following fields for each memory:
    - memory_type: one of ["ongoing_theme", "coping_strategy", "personal_goal", "relationship_context", "stress_trigger", "positive_progress", "open_loop", "preference"]
    - summary: str
    - emotional_tone: str
    - importance: int 1-5
    - stability: one of ["one_time", "recurring", "unknown"]
    - sensitivity: one of ["low", "medium", "high"]
    - actionability: one of ["low", "medium", "high"]
    - open_loop: bool
    - follow_up_suggestion: Optional[str]
    - do_not_use_for_push: bool

Data:
{data}
"""

SESSION_OPENER_PROMPT = """
Generate the first message in a new session for a mental-health support AI based on the following retrieved memories.

Retrieved Memories:
{memories}

Instructions:
- Use selected memories naturally and gently.
- Do not sound like a database.
- Do not mention "memory", "stored", "record", or "previous session data".
- Do not overstate certainty.
- Do not be clinical.
- Do not pressure the user.
- Ask one open-ended question.
- Under 80 words.
- Sound warm and human.

Example of good tone:
"Welcome back. Last time, that team meeting seemed to be taking up a lot of space. I’m curious how the week has felt since then — especially whether the grounding exercise helped at all."
"""
