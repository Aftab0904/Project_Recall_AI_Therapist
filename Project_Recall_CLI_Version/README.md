# Project Recall - CLI Version

> **One-line thesis:** This prototype remembers only what is useful for care continuity, retrieves only what is safe and relevant, and uses memory to make the next session feel human without turning emotional vulnerability into a retention lever.

## Overview
Project Recall CLI is a minimal but functional prototype for an AI therapist memory and re-engagement system. It demonstrates how to handle sensitive therapeutic context using a privacy-aware, structured memory architecture.

## What this Prototype Demonstrates
- **Structured Extraction:** Moving away from raw transcripts to summarized, categorized memories.
- **Privacy Controls:** Handling sensitivity levels and "do not use for push" flags.
- **Weighted Retrieval:** A scoring algorithm that prioritizes importance, recency, and open loops.
- **Human-Centric UX:** Generating warm, non-robotic openers under 80 words.

## Tech Stack
- **Language:** Python 3.10+
- **CLI Framework:** Typer
- **Data Validation:** Pydantic v2
- **Terminal UI:** Rich
- **LLM Client:** OpenRouter (Mock mode included)

## Setup Instructions

1. **Navigate to folder:**
   ```bash
   cd Project_Recall_CLI_Version
   ```

2. **Create and activate Virtual Environment:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file based on `.env.example`. By default, `MOCK_LLM=true` is set so no API key is required.

## How to Run
Run the full end-to-end demo to see the system in action:
```bash
python -m app.cli demo
```

### Individual Commands:
- **Ingest Sessions:** `python -m app.cli ingest data/sample_sessions.json`
- **Show Memories:** `python -m app.cli memories --user demo_user`
- **Generate Opener:** `python -m app.cli open-session --user demo_user`
- **Run Notifications:** `python -m app.cli notifications --user demo_user`

## Demo Screenshots
Here is how the CLI version looks in action:

![CLI Demo 1](../assets/Screenshot%20(270).png)
![CLI Demo 2](../assets/Screenshot%20(271).png)
![CLI Demo 3](../assets/Screenshot%20(274).png)

## Architecture & Design
Refer to `design_doc.md` for the retrieval logic details and `ethics.md` for the risk analysis.

## Why CLI Only?
This prototype focuses on the **logic and safety** of memory management. By removing the complexity of a web frontend or LangGraph, we maintain a clean, high-signal codebase that demonstrates the core engineering challenges of therapeutic AI memory.
