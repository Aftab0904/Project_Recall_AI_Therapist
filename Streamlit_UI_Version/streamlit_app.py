import streamlit as st
import json
import time
import os
import pandas as pd
from datetime import datetime

from app.schemas import Session, Memory, MemoryType
from app.llm_client import llm_client
from app.memory_store import memory_store
from app.memory_extractor import memory_extractor
from app.retrieval import retriever
from app.notifications import notification_engine
from app.evaluation import evaluator
from app.prompts import SESSION_OPENER_PROMPT, CHAT_RESPONSE_PROMPT, EVALUATION_EXPLANATION_TEXT
from app.sample_data import EXPECTED_MEMORIES_COUNT

# Page configuration
st.set_page_config(
    page_title="Project Recall: Contextual Memory Prototype",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional look (no emojis)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }

    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        border: 1px solid #4CAF50;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 52px;
        white-space: pre-wrap;
        background-color: #dfe7ef;
        color: #1f2937;
        border-radius: 8px 8px 0px 0px;
        border: 1px solid #b8c4d0;
        padding: 10px 18px;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #cbd8e6;
        color: #111827;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2e7d32 !important;
        color: white !important;
        border: 1px solid #2e7d32;
    }

    .stTabs [aria-selected="true"] p {
        color: white !important;
    }

    .stTabs [data-baseweb="tab"] p {
        color: #1f2937;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_opener' not in st.session_state:
    st.session_state.last_opener = None
if 'last_retrieved' not in st.session_state:
    st.session_state.last_retrieved = []
if 'last_generation_source' not in st.session_state:
    st.session_state.last_generation_source = "None"
if 'last_latency' not in st.session_state:
    st.session_state.last_latency = {"retrieval": 0, "generation": 0}

USER_ID = "demo_user"

# Sidebar
st.sidebar.title("Project Recall")
st.sidebar.subheader("System Status")

status = llm_client.get_status()
st.sidebar.text(f"Provider: {status['provider']}")
st.sidebar.text(f"Model: {status['model']}")
st.sidebar.text(f"Mock mode: {status['mock_mode']}")
st.sidebar.text(f"API key detected: {'Yes' if status['api_key_detected'] else 'No'}")
st.sidebar.text(f"Last source: {st.session_state.last_generation_source}")

memories = memory_store.get_memories(USER_ID)
st.sidebar.text(f"Memory count: {len(memories)}")
st.sidebar.text(f"User ID: {USER_ID}")

st.sidebar.divider()
st.sidebar.subheader("Demo Controls")

if st.sidebar.button("Reset demo"):
    memory_store.reset()
    st.session_state.chat_history = []
    st.session_state.last_opener = None
    st.session_state.last_retrieved = []
    st.sidebar.success("Demo reset successfully")
    st.rerun()

if st.sidebar.button("Ingest sample sessions"):
    with st.spinner("Ingesting sessions..."):
        # Load samples from file
        with open("data/sample_sessions.json", "r", encoding="utf-8") as f:
            samples = json.load(f)
        
        total_extracted = 0
        for s in samples:
            # Join key moments for extraction
            transcript = f"Theme: {s['theme']}. Moments: {' '.join(s['key_moments'])}"
            count = memory_extractor.extract_memories(USER_ID, transcript, mock=status['mock_mode'])
            total_extracted += count
        
        st.sidebar.success(f"Ingested {len(samples)} sessions, extracted {total_extracted} memories")
        st.rerun()

# Sample Session Data for display
def load_sample_sessions():
    with open("data/sample_sessions.json", "r") as f:
        return json.load(f)

sample_sessions = load_sample_sessions()

# Sidebar display of history
st.sidebar.divider()
st.sidebar.subheader("Input Session History")
for s in sample_sessions:
    with st.sidebar.expander(f"{s['session_id']}: {s['theme']}"):
        st.text(f"Tone: {s['emotional_tone']}")
        st.text(f"Close: {s['closing_state']}")
        for m in s['key_moments']:
            st.text(f"- {m}")

# Main Page
st.title("Project Recall: Contextual Memory Prototype")

tabs = st.tabs([
    "Session History", 
    "Memory Store", 
    "Session Opener", 
    "Chat Simulation", 
    "Re-engagement Logic", 
    "Evaluation", 
    "Architecture & Ethics"
])

# Tab 1: Session History
with tabs[0]:
    st.header("Simulated Session History Store")
    st.write("This tab shows the raw input transcripts available in the system for the demo user.")
    
    for s in sample_sessions:
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.metric("Session", s['session_id'])
                st.text(s['timestamp'].split('T')[0])
            with col2:
                st.subheader(s['theme'])
                st.write(f"Emotional Tone: {s['emotional_tone']}")
                st.write(f"Closing State: {s['closing_state']}")
                st.write("Key Moments:")
                for m in s['key_moments']:
                    st.write(f"- {m}")
            st.divider()

# Tab 2: Memory Store
with tabs[1]:
    st.header("Structured Memory Store")
    st.write("The prototype stores structured memory summaries rather than raw transcripts for efficiency and privacy.")
    
    if not memories:
        st.info("No memories yet. Click Ingest sample sessions in the sidebar to begin.")
    else:
        # Sort memories by importance desc, then updated_at desc
        sorted_memories = sorted(memories, key=lambda x: (x.importance, x.updated_at), reverse=True)
        
        mem_data = []
        for m in sorted_memories:
            mem_data.append({
                "ID": m.memory_id,
                "Type": m.memory_type.value,
                "Summary": m.summary,
                "Tone": m.emotional_tone,
                "Imp": m.importance,
                "Stability": m.stability,
                "Sens": m.sensitivity,
                "Action": m.actionability,
                "Open": "Yes" if m.open_loop else "No",
                "No Push": "Yes" if m.do_not_use_for_push else "No",
                "Date": m.updated_at.strftime("%Y-%m-%d")
            })
        
        st.table(pd.DataFrame(mem_data))

# Tab 3: Session Opener
with tabs[2]:
    st.header("Context-Aware Session Opener")
    st.write("Generate a warm, human message to start a new session based on previous context.")
    
    if st.button("Generate session opener"):
        if not memories:
            st.warning("Please ingest sample sessions first.")
        else:
            with st.spinner("Retrieving context and generating message..."):
                start_time = time.time()
                # Retrieve top 2 memories for opener (no specific query)
                retrieved = retriever.retrieve_memories("", memories, limit=2)
                retrieval_latency = (time.time() - start_time) * 1000
                
                # Format for prompt
                mem_context = "\n".join([f"- {r['summary']}" for r in retrieved])
                prompt = SESSION_OPENER_PROMPT.format(memories=mem_context)
                
                gen_start = time.time()
                response = llm_client.chat_completion([{"role": "user", "content": prompt}])
                gen_latency = (time.time() - gen_start) * 1000
                
                message = response["content"]
                if not message:
                    # Fallback
                    message = f"Welcome back. Last time we talked about {retrieved[0]['theme'].lower()}. How has that been feeling for you since then?"
                
                st.session_state.last_opener = message
                st.session_state.last_retrieved = retrieved
                st.session_state.last_generation_source = response["source"]
                st.session_state.last_latency = {"retrieval": retrieval_latency, "generation": gen_latency}
                
                st.rerun()

    if st.session_state.last_opener:
        st.subheader("Generated Opener")
        st.info(st.session_state.last_opener)
        
        st.subheader("Retrieval Transparency")
        for r in st.session_state.last_retrieved:
            with st.expander(f"Memory: {r['theme']} (Score: {r['score']})"):
                st.write(f"Summary: {r['summary']}")
                st.write("Score Components:")
                st.json(r['explanation'])
    else:
        st.info("Click the button to generate a new session opener.")

# Tab 4: Chat Simulation
with tabs[3]:
    st.header("Contextual Chat Simulation")
    st.write("Type a message to see how Mentra uses past memories to provide a specific, helpful response.")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.chat_message("user").write(chat["content"])
        else:
            st.chat_message("assistant").write(chat["content"])
            if "retrieved" in chat:
                with st.expander("Retrieved context for this response"):
                    for r in chat["retrieved"]:
                        st.text(f"- {r['summary']} (Score: {r['score']})")

    if prompt := st.chat_input("How can I improve my work-life balance?"):
        if not memories:
            st.warning("Please ingest sample sessions first.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            with st.spinner("Thinking..."):
                # Multi-turn context resolution
                last_user_msgs = [c["content"] for c in st.session_state.chat_history if c["role"] == "user"][-3:]
                retrieval_query = " ".join(last_user_msgs)
                
                start_time = time.time()
                retrieved = retriever.retrieve_memories(retrieval_query, memories, limit=3)
                retrieval_latency = (time.time() - start_time) * 1000
                
                # Generation
                mem_context = "\n".join([f"- {r['summary']}" for r in retrieved])
                chat_history_str = "\n".join([f"{c['role']}: {c['content']}" for c in st.session_state.chat_history[-5:]])
                
                gen_prompt = CHAT_RESPONSE_PROMPT.format(
                    user_message=prompt,
                    memories=mem_context,
                    history=chat_history_str
                )
                
                gen_start = time.time()
                response = llm_client.chat_completion([{"role": "user", "content": gen_prompt}])
                gen_latency = (time.time() - gen_start) * 1000
                
                message = response["content"]
                if not message:
                    # Fallback logic based on keywords
                    p_lower = prompt.lower()
                    if any(kw in p_lower for kw in ["work", "balance", "boundaries"]):
                        message = "If the main issue is work-life balance, I would start with one small boundary rather than trying to change everything at once. You could choose a shutdown ritual, turn off work notifications after a set time, or prepare one sentence for saying no. Which part feels hardest right now: stopping work, saying no, or mentally switching off?"
                    elif "sleep" in p_lower:
                        message = "Sleep seems connected to rumination for you, especially replaying work conversations early in the morning. A useful first step could be moving the worry out of your head before bed: write tomorrow's concerns on paper, then choose one small wind-down routine. What usually starts the 4 AM spiral?"
                    else:
                        message = "I hear you. To make this useful, we can narrow it to one part of the week that felt heavy, or one small next step you'd like to try. What feels most present for you?"

                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": message, 
                    "retrieved": retrieved
                })
                
                st.session_state.last_generation_source = response["source"]
                st.session_state.last_latency = {"retrieval": retrieval_latency, "generation": gen_latency}
                st.rerun()

# Tab 5: Re-engagement Logic
with tabs[4]:
    st.header("Rule-Based Re-engagement Logic")
    st.write("This panel shows how the system decides when to send push notifications based on care continuity signals.")
    
    scenarios = notification_engine.get_notification_scenarios(memories)
    
    for sc in scenarios:
        with st.expander(f"Scenario: {sc['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Signals**")
                for s in sc['signals']:
                    st.text(f"- {s}")
                st.write(f"**Decision**: {sc['decision']}")
            with col2:
                st.write("**Notification Copy**")
                st.info(sc['copy'])
            st.write(f"**Safety Rationale**: {sc['safety_rationale']}")
    
    st.divider()
    st.subheader("Safety Gates")
    st.write("- No push notifications for crisis-related signals.")
    st.write("- High-sensitivity memories (e.g., trauma) are excluded from push.")
    st.write("- Frequency cap: maximum 1 re-engagement per 3 days.")
    st.write("- Language is strictly low-pressure and supportive.")

# Tab 6: Evaluation
with tabs[5]:
    st.header("Evaluation Summary")
    st.write(EVALUATION_EXPLANATION_TEXT)
    
    if not memories:
        st.info("No data to evaluate. Please ingest sample sessions and generate an opener.")
    else:
        # 1. Memory Coverage
        cov = evaluator.calculate_extraction_coverage(len(memories), EXPECTED_MEMORIES_COUNT)
        st.subheader("1. Memory Extraction Coverage")
        col1, col2, col3 = st.columns(3)
        col1.metric("Expected", cov['expected'])
        col2.metric("Extracted", cov['extracted'])
        col3.metric("Score", f"{cov['score']}%")
        st.progress(cov['score'] / 100)
        
        # 2. Retrieval Recall @ 3
        st.divider()
        st.subheader("2. Retrieval Recall @ 3")
        recall = evaluator.calculate_retrieval_recall(retriever, memories)
        st.metric("Recall @ 3 Score", f"{recall['score']}%")
        
        recall_df = []
        for d in recall['details']:
            recall_df.append({
                "Query": d['query'],
                "Pass": "Pass" if d['pass'] else "Fail"
            })
        st.table(pd.DataFrame(recall_df))
        
        # 3. Human Recall Score
        st.divider()
        st.subheader("3. Human Recall Score")
        if st.session_state.last_opener:
            # Get retrieved summaries for specificity check
            ret_sums = [r['summary'] for r in st.session_state.last_retrieved]
            hrs = evaluator.calculate_human_recall_score(st.session_state.last_opener, ret_sums)
            
            col1, col2, col3 = st.columns(3)
            col1.write(f"Warmth: {'Pass' if hrs['warmth_pass'] else 'Fail'}")
            col2.write(f"Specificity: {'Pass' if hrs['specificity_pass'] else 'Fail'}")
            col3.metric("Human Recall Score", f"{hrs['score']}%")
            st.info(f"Evaluated Opener: {st.session_state.last_opener}")
        else:
            st.info("Generate a session opener to see human recall metrics.")
            
        # 4. Safety Filter
        st.divider()
        st.subheader("4. Safety Filter")
        safety = evaluator.calculate_safety_filter(st.session_state.last_retrieved)
        col1, col2, col3 = st.columns(3)
        col1.metric("High-Sensitivity", safety['high_sensitivity_used'])
        col2.metric("Push Violations", safety['push_violations'])
        col3.metric("Status", safety['status'])
        
        # 5. Latency
        st.divider()
        st.subheader("5. Latency")
        lat = evaluator.get_latency_metrics(
            st.session_state.last_latency['retrieval'], 
            st.session_state.last_latency['generation']
        )
        col1, col2, col3, col4 = st.columns(4)
        col1.text(f"Retrieval: {round(lat['retrieval'], 1)} ms")
        col2.text(f"Generation: {round(lat['generation'], 1)} ms")
        col3.metric("Total Latency", f"{round(lat['total'], 1)} ms")
        col4.metric("Status", lat['status'])
        st.write("Target: under 2000 ms")

# Tab 7: Architecture & Ethics
with tabs[6]:
    st.header("Architecture and Ethics")
    
    st.subheader("Memory Architecture")
    st.write("""
    The system uses a **durable memory pipeline** that separates transient chat noise from structured therapeutic context.
    - **Extraction**: Post-session asynchronous extraction of core themes and goals.
    - **Deduplication**: Fingerprint-based hashing (user + theme + summary) ensures each pattern is stored only once.
    - **Retrieval**: Weighted keyword scoring (Overlap + Importance + Recency + Open Loops).
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**What we store**")
        st.write("- Structured summaries")
        st.write("- Emotional tone and themes")
        st.write("- Importance and sensitivity scores")
        st.write("- Open loop signals")
    with col2:
        st.write("**What we do NOT store**")
        st.write("- Raw session audio/video")
        st.write("- Personally identifiable third-party names")
        st.write("- Irrelevant conversational tangents")
        st.write("- Unverified clinical diagnoses")
        
    st.divider()
    st.subheader("Ethical Risk Analysis")
    st.write("""
    **Top 3 Risks**
    1. **Creepy or overconfident recall**: AI sounding like a surveillance tool.
    2. **Privacy harm**: Sensitive data exposure or misuse for re-engagement.
    3. **Emotional over-dependency**: AI acting as a replacement for human care.

    **Mitigations**
    - **Human-in-the-loop tone**: Opener prompts are strictly tuned for warmth and curiosity, not factual reporting.
    - **Safety Gates**: Sensitive memories are explicitly flagged and excluded from push notifications.
    - **Transparency**: Users can see and control exactly what the system remembers (demonstrated in the Memory Store tab).
    """)
