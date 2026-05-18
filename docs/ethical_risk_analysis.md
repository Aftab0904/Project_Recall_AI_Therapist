# Ethical Risk Analysis: Contextual Memory in Mental Health

## Top 3 Risks

### 1. Privacy Leakage and Unwanted Recall
**Risk**: The AI recalls a sensitive or traumatic event at an inappropriate time, causing distress or "algorithmic gaslighting" where the AI reinforces a negative memory.
**Mitigation**: We implement a **Sensitivity Guardrail**. Memories flagged as "High" or "Critical" sensitivity are excluded from automated warm openers. Users also have a "Forget" feature to wipe specific themes.

### 2. Emotional Dependency and Manipulative Re-engagement
**Risk**: Personalized push notifications could create an unhealthy dependency on the AI or feel manipulative (e.g., "I know you were sad yesterday, come talk to me").
**Mitigation**: **Rule-Based Constraints**. Notifications are limited to a max of 1 per week and use "gentle, non-intrusive" copy. Triggers focus on "checking in on a plan" rather than "leveraging negative emotion."

### 3. False Memory Reinforcement
**Risk**: If the LLM incorrectly extracts a memory (e.g., "You said you hate your brother" when the user said "My brother is having a hard time"), the AI might reinforce a false narrative.
**Mitigation**: **Transparency Panel**. By showing the user exactly what is remembered in a "Memory Sidebar," the user can correct or delete inaccurate summaries.

## Clinical/Ethics Flags
Before deploying to real users, I would flag the following for clinical review:
- **Crisis Workflow**: Ensuring that any mention of self-harm in a memory extraction is routed to a human/crisis line immediately, bypassing the vector store.
- **Memory Decay**: Defining a clinical policy for when memories should naturally "fade" or be archived to avoid over-referencing the distant past.
- **Consent**: Creating a clear, multi-modal consent screen for "Contextual Memory" usage.
