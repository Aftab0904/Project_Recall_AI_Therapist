# Memory Architecture Design

## Memory Schema
The system extracts and stores **structured memory summaries** rather than raw transcripts. 

### Schema Components
- **summary**: Concise, objective description of the pattern or goal.
- **memory_type**: Categorization (e.g., `stress_trigger`, `coping_strategy`, `personal_goal`).
- **emotional_tone**: The primary emotion associated with the memory.
- **importance**: 1-10 weight to prioritize recall.
- **stability**: Whether the pattern is `recurring` or a `one_time` event.
- **open_loop**: Boolean indicating if there is unresolved tension requiring follow-up.
- **sensitivity**: Risk level (`low`, `medium`, `high`) to gate retrieval and push notifications.

### Rationale
Storing raw transcripts is noisy and privacy-invasive. Structured memories act as "therapeutic anchors" that allow the AI to maintain continuity without re-reading thousands of words.

## Retrieval Strategy
The prototype uses a **weighted keyword retrieval** system.
- **Scoring**: `Score = (Keyword Overlap * 10) + (Importance * 0.5) + Recency + Open Loop Bonus - Sensitivity Penalty`.
- **Latency**: Keyword matching on small JSON stores is extremely fast (< 10ms), ensuring no degradation in session-start latency.
- **Context Resolution**: The system combines the current user message with the last 2 turns to resolve pronouns (e.g., "it" referring to "work-life balance").

## Privacy and User Control
- **Deduplication**: Fingerprint-based hashing prevents the storage of redundant emotional data.
- **Transparency**: The "Memory Store" tab demonstrates how users can see exactly what the AI remembers.
- **Selective Forget**: In production, each memory would have a "Forget" button to purge it from the store.

## What NOT to Store
- **Names and Identifiers**: PII of third parties mentioned in sessions.
- **Transient Noise**: Conversational filler or unrelated tangents.
- **Unverified Diagnosis**: The AI should store observations ("User feels anxious"), not medical labels ("User has GAD").
- **High-Risk Crisis Content**: Raw details of self-harm or crisis are routed to safety protocols rather than durable memory.
