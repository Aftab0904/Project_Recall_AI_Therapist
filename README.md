# Project Recall: Mentra AI Therapist Memory System

Project Recall is a portfolio-defining contextual memory and re-engagement system for Mentra, an AI therapist. It focuses on privacy-first, safety-aware memory extraction and retrieval to make users feel remembered without being robotic or invasive.

## Why This Project Matters
In mental health applications, "feeling remembered" is a key driver of therapeutic alliance and retention. However, naive RAG (Retrieval-Augmented Generation) can lead to "uncanny valley" experiences where the AI parrots sensitive facts without emotional nuance. This project implements a structured, multi-tiered memory architecture to ensure relevance, safety, and warmth.

## Architecture Diagram
```
[User Session] -> [LangGraph Ingestion] 
                        |
                        v
          [Safety Filter & Memory Extraction]
                        |
            /-----------+-----------\
           v                         v
    [SQLite Metadata]        [ChromaDB Vector Store]
    (Privacy & Control)      (Semantic Search)
           \-----------+-----------/
                        |
           [Weighted Re-ranking & Retrieval]
                        |
            [LangGraph Warm Opener Gen] -> [Warm Session Message]
```

## Tech Stack
- **Backend**: Python 3.11, FastAPI, LangGraph, SQLAlchemy (SQLite), ChromaDB, Pydantic v2
- **Frontend**: React 19, Vite, TypeScript, Tailwind CSS, Lucide Icons
- **LLM**: DeepSeek-R1 (Local via Ollama or OpenRouter)
- **Testing**: Pytest, Pytest-asyncio

## Setup Instructions

### Backend
1. `cd backend`
2. `python -m venv .venv`
3. `source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `cp .env.example .env`
6. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Open [http://localhost:3000](http://localhost:3000)

### LLM Options
- **Mock Mode**: Set `LLM_PROVIDER=mock` in `.env`. No API key or local model needed.
- **Ollama**: Install Ollama, run `ollama pull deepseek-r1:7b`, and set `LLM_PROVIDER=ollama`.
- **OpenRouter**: Set `LLM_PROVIDER=openrouter` and add your `OPENROUTER_API_KEY`.

## Demo Flow
1. **Reset Demo**: `POST /api/demo/reset` (Clears DBs)
2. **Ingest Samples**: `POST /api/ingest` (Ingests 5 simulated therapy sessions)
3. **Start Session**: `POST /api/session/start` (Retrieves memories and generates warm opener)
4. **View Memories**: `GET /api/memories/demo_user` (Transparency panel)
5. **Forget Memory**: `POST /api/memories/exclude` (User-controlled deletion)
6. **Trigger Notification**: `POST /api/notifications/trigger` (Rule-based re-engagement)

## Privacy-First Design
- **Multi-tiered Memory**: Distinguishes between stable core profile facts and ephemeral session themes.
- **Explicit Exclusions**: Users can mark content to be "forgotten," which triggers immediate removal from vector search.
- **No Raw Storage**: Transcripts are processed for memories and then only metadata/summaries are stored long-term.

## Known Limitations
- The current re-ranking logic is a simplified weighted sum.
- Safety filtering relies on LLM classification, which should be augmented by keyword-based clinical rules in production.

## What I would build with 2 more weeks
- **Evaluation Harness**: Framework to score "warmth" and "relevance" using a clinical judge model.
- **Graph-based Relationships**: Linking themes across sessions (e.g., how "Work Anxiety" relates to "Sleep Issues").
- **Human-in-the-Loop**: A dashboard for clinical reviewers to audit memory extraction.
- **Front-end**: A React-based UI to demonstrate the conversational flow and memory transparency.
