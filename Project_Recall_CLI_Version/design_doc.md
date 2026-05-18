# Design Document: Project Recall

## Objective
To provide a lightweight, privacy-aware memory system for therapeutic AI applications, ensuring continuity without compromising sensitive user data.

## Core Components

1. **Memory Extractor:** Uses an LLM to identify key insights, milestones, and emotional states from session transcripts.
2. **Memory Store:** A JSON-based local storage for memories, keyed by user ID.
3. **Retrieval Engine:** A scoring system that selects relevant memories based on recency, emotional depth, and safety.
4. **Safety Layer:** Filters memories to ensure no harmful or triggering content is retrieved for session openings.
5. **Notification System:** Generates re-engagement scenarios based on stored memories.

## Data Schema
- **Memory:** ID, UserID, Timestamp, Category (Insight, Milestone, Emotional State), Content, SafetyScore (0-1), ImportanceScore (0-1).

## Workflow
1. Ingest session transcript.
2. Extract atomic memories.
3. Score and store.
4. Retrieve top-N safe memories for next session.
5. Generate a warm, contextual opening message.
