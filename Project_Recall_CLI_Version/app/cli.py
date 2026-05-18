import typer
import json
import os
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from .schemas import Session, Memory
from .llm_client import LLMClient
from .memory_extractor import MemoryExtractor
from .memory_store import MemoryStore
from .retrieval import MemoryRetriever
from .notifications import NotificationEngine
from .prompts import SESSION_OPENER_PROMPT

app = typer.Typer(help="Project Recall - Privacy-Aware Contextual Memory for Therapeutic Continuity")
console = Console()

@app.command()
def ingest(file_path: str):
    """Ingest sessions from a JSON file and extract memories."""
    if not os.path.exists(file_path):
        console.print(f"[red]Error: File {file_path} not found.[/red]")
        raise typer.Exit(1)

    with open(file_path, "r") as f:
        data = json.load(f)
    
    sessions = [Session(**s) for s in data]
    llm = LLMClient()
    extractor = MemoryExtractor(llm)
    store = MemoryStore()

    console.print(f"Ingesting {len(sessions)} sessions...")
    total_memories = 0
    for session in sessions:
        memories = extractor.extract_memories(session)
        store.add_memories(memories)
        total_memories += len(memories)
    
    console.print(f"[green]Successfully processed {len(sessions)} sessions and extracted {total_memories} memories.[/green]")

@app.command()
def memories(user: str = "demo_user"):
    """Show stored memories for a specific user."""
    store = MemoryStore()
    user_memories = store.get_user_memories(user)
    
    if not user_memories:
        console.print(f"[yellow]No memories found for user {user}.[/yellow]")
        return

    table = Table(title=f"Memories for {user}")
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Summary")
    table.add_column("Tone", style="green")
    table.add_column("Imp.", justify="center")
    table.add_column("Sens.", justify="center")
    table.add_column("Open", justify="center")
    table.add_column("No Push", justify="center")

    for m in user_memories:
        table.add_row(
            m.memory_id,
            m.memory_type,
            m.summary,
            m.emotional_tone,
            str(m.importance),
            m.sensitivity,
            "Yes" if m.open_loop else "No",
            "Yes" if m.do_not_use_for_push else "No"
        )
    
    console.print(table)

@app.command()
def open_session(user: str = "demo_user"):
    """Retrieve memories and generate a warm session opener."""
    store = MemoryStore()
    user_memories = store.get_user_memories(user)
    
    if not user_memories:
        console.print(f"[yellow]No memories found for user {user}. Please ingest data first.[/yellow]")
        return

    retriever = MemoryRetriever(user_memories)
    top_memories = retriever.get_top_memories(user)
    
    console.print("[bold underline]Retrieved Contextual Memories:[/bold underline]")
    for i, m in enumerate(top_memories):
        console.print(f"{i+1}. [cyan]{m.summary}[/cyan] (Type: {m.memory_type})")

    llm = LLMClient()
    memories_text = "\n".join([f"- {m.summary} ({m.emotional_tone})" for m in top_memories])
    prompt = SESSION_OPENER_PROMPT.format(memories=memories_text)
    opener = llm.chat(prompt)
    
    console.print("\n[bold green]Warm Opening Message:[/bold green]")
    console.print(f'"{opener}"')
    
    word_count = len(opener.split())
    if word_count > 80:
        console.print(f"\n[yellow]Note: Message is {word_count} words (limit is 80).[/yellow]")

@app.command()
def notifications(user: str = "demo_user"):
    """Run notification/re-engagement logic and show examples."""
    engine = NotificationEngine()
    scenarios = engine.get_example_scenarios()
    
    table = Table(title=f"Notification Scenarios for {user}")
    table.add_column("Scenario", style="bold")
    table.add_column("Signals")
    table.add_column("Copy", style="italic")
    table.add_column("Safety Rationale")

    for s in scenarios:
        table.add_row(
            s["scenario"],
            s["signals"],
            s["copy"],
            s["why_safe"]
        )
    
    console.print(table)

@app.command()
def demo():
    """Run the full end-to-end demo flow."""
    store = MemoryStore()
    store.clear()
    
    console.print("[bold blue]Starting Full Project Recall Demo[/bold blue]\n")
    
    # 1. Ingest
    console.print("[bold]1. Ingesting sessions from data/sample_sessions.json...[/bold]")
    ingest("data/sample_sessions.json")
    
    # 2. Show memories
    console.print("\n[bold]2. Displaying extracted memories...[/bold]")
    memories("demo_user")
    
    # 3. Generate opener
    console.print("\n[bold]3. Generating warm session opener...[/bold]")
    open_session("demo_user")
    
    # 4. Show notifications
    console.print("\n[bold]4. Running notification logic examples...[/bold]")
    notifications("demo_user")
    
    console.print("\n[bold green]Demo Complete Success![/bold green]")

if __name__ == "__main__":
    app()
