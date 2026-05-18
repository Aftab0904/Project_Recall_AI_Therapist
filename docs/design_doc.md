# Design Document: Memory RAG Lite

## Overview
Mentra's memory system avoids "naive RAG" by implementing a structured extraction and retrieval pipeline. Instead of embedding entire transcripts, we extract safe, summarized "memories" that are categorized by type and sensitivity.

## Information Extraction (Schema)
For each session, we extract:
- **Summary**: A safe, non-clinical summary of the theme.
- **Memory Type**: `core_profile` (stable) or `session_ephemeral` (short-term).
- **Importance**: 1-10 scale for re-ranking.
- **Sensitivity**: Low/Medium/High to prevent referencing highly sensitive trauma in casual openers.
- **Theme**: Categorical label (e.g., Work, Family, Self-Care).

**Rationale**: Storing structured summaries rather than raw text reduces "hallucination" risk and ensures that the AI only references pre-approved, safe concepts.

## Storage Strategy
- **SQLite**: Stores the source of truth, including deletion status, importance scores, and timestamps.
- **ChromaDB**: Stores embeddings of the *summaries* only for semantic retrieval.
- **Consistency**: The `memory_id` links the two stores. When a memory is deleted in SQLite, it is immediately removed from ChromaDB.

## Retrieval & Re-ranking
At the start of a session, we retrieve the top 10 candidates from ChromaDB and re-rank them using:
`Score = (Similarity * 0.4) + (Importance * 0.3) + (Recency * 0.2) + (Unresolved_Bonus * 0.1)`

Only the top 2-3 memories are passed to the LLM to minimize latency and context window clutter.

## Privacy & User Control
- **Exclusion List**: If a user says "I don't want to talk about my boss anymore," that phrase is added to an exclusion list. Semantic search is then used to find and soft-delete related memories.
- **Transparency**: The API provides a full list of "What the AI remembers," which can be exposed in a UI for user audit.
- **What is NOT stored**: 
    - Raw session transcripts (deleted after extraction).
    - Precise quotes (to avoid mimicking/mocking).
    - Clinical diagnoses or labels (e.g., "User has GAD").
