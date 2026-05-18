# Project Recall: Contextual Memory & Re-engagement System

Project Recall is a sophisticated, privacy-first contextual memory system designed to bridge the gap between robotic data retrieval and genuine human-centric interaction. Built for high-empathy applications, it utilizes an advanced agentic architecture to ensure users feel understood and remembered without compromising safety or privacy.

---

## Key Skills & Tech Stack

| Category | Technologies |
| :--- | :--- |
| Agentic Framework | LangGraph, LangChain |
| Core AI / LLM | DeepSeek-R1 (via Ollama/OpenRouter), LLM-based Safety Filtering |
| Retrieval Architecture | Advanced RAG, Semantic Search, Custom Re-ranking Algorithms |
| Backend Orchestration | Python 3.11, FastAPI, Pydantic v2 |
| Database & Storage | ChromaDB (Vector Store), SQLAlchemy (SQLite - Metadata) |
| Frontend Interaction | React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons |
| Testing & Quality | Pytest, Pytest-asyncio |

---

## Why This Project Matters

In the world of AI, "feeling remembered" is the foundation of trust. However, traditional RAG (Retrieval-Augmented Generation) often falls into the "uncanny valley"—parroting sensitive facts back to the user in cold, awkward ways. 

Project Recall implements a Multi-tiered Memory Architecture that distinguishes between what someone is (core profile) and what someone is feeling (session themes). This creates a "Warm Opener" experience that mimics human memory: relevant, emotionally aware, and respectful of boundaries.

---

## System Architecture

The following diagram shows how the system processes information and remembers key details for future conversations.

```mermaid
graph TD
    %% Node Definitions
    Input[New User Message]
    
    subgraph Processing [Step 1: Understanding & Safety]
        LangGraph{LangGraph Orchestrator}
        Safety[Safety Filter & Sensitivity Audit]
    end

    subgraph Memory [Step 2: Storing Memories]
        Extraction[Memory Extraction Agent]
        SQL[(SQLite: Metadata & Control)]
        Chroma[(ChromaDB: Vector Store)]
    end

    subgraph Retrieval [Step 3: Remembering & Greeting]
        Search[Semantic Search & RAG]
        Ranker[Custom Re-ranking Logic]
        Greeting[Warm Opener Generation]
    end

    Output[Personalized Welcome Message]

    %% Connections
    Input --> LangGraph
    LangGraph --> Safety
    Safety --> Extraction
    Extraction --> SQL
    Extraction --> Chroma
    
    SQL --> Search
    Chroma --> Search
    Search --> Ranker
    Ranker --> Greeting
    Greeting --> Output

    %% Styling
    style LangGraph fill:#f9f,stroke:#333,stroke-width:2px,color:#000
    style Safety fill:#ff9,stroke:#333,stroke-width:2px,color:#000
    style Extraction fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style SQL fill:#9ff,stroke:#333,stroke-width:2px,color:#000
    style Chroma fill:#9ff,stroke:#333,stroke-width:2px,color:#000
    style Search fill:#f99,stroke:#333,stroke-width:2px,color:#000
    style Ranker fill:#f99,stroke:#333,stroke-width:2px,color:#000
    style Greeting fill:#bbf,stroke:#333,stroke-width:2px,color:#000
```

---

## Features

- Privacy-First "Right to be Forgotten": Users can explicitly exclude topics. The system performs a cascading delete across both vector and relational stores.
- Sensitivity-Aware Retrieval: High-sensitivity memories (e.g., trauma) are filtered out of casual re-engagement to prevent emotional distress.
- Dynamic Re-ranking: Memories aren't just retrieved by similarity; they are scored based on Recency, Importance, and Unresolved Themes.
- Transparency Panel: A dedicated UI section allows users to see exactly what the AI remembers about them, putting control back into their hands.

---

## Demo Screenshots

| Memory Transparency & Chat | Simulation Controls |
| :---: | :---: |
| ![Chat and Memory View](assets/Screenshot%20(270).png) | ![Control Panel](assets/Screenshot%20(271).png) |

| Advanced Safety Audit |
| :---: |
| ![Safety Metrics](assets/Screenshot%20(274).png) |

---

## Setup Instructions

### Backend
1. cd backend
2. python -m venv .venv
3. source .venv/bin/activate (or .\.venv\Scripts\activate on Windows)
4. pip install -r requirements.txt
5. cp .env.example .env
6. uvicorn app.main:app --reload

### Frontend
1. cd frontend
2. npm install
3. npm run dev

---

## Demo Flow
1. Reset Demo: POST /api/demo/reset (Clears DBs)
2. Ingest Samples: POST /api/ingest (Ingests 5 simulated sessions)
3. Start Session: POST /api/session/start (Retrieves memories and generates warm opener)
4. View Memories: GET /api/memories/demo_user (Transparency panel)
5. Forget Memory: POST /api/memories/exclude (User-controlled deletion)
