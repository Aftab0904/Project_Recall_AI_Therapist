# Ethical Risk Analysis

## Top 3 Risks

1. **Creepy or Overconfident Recall**
AI "reporting" past data back to a user can feel invasive and robotic, breaking the therapeutic alliance. It turns a vulnerable conversation into a data readout.
*Mitigation*: Opener prompts are explicitly tuned for curiosity and warmth. We avoid saying "I see in my records..." and instead use phrases like "I was thinking about our last talk...".

2. **Privacy Harm from Sensitive Data**
Mental health data is highly sensitive. Storing summaries that are too detailed or using them for poorly timed re-engagement can cause distress.
*Mitigation*: We implement "Safety Gates" that exclude high-sensitivity memories from push notifications and use a "Deduplication Fingerprint" to minimize the volume of stored data.

3. **Manipulative Re-Engagement**
Using a user's anxiety or unresolved trauma as a lever to drive app engagement is unethical and clinically risky.
*Mitigation*: Notification scenarios are strictly limited to low-pressure, supportive check-ins. No crisis-related push notifications are allowed, and re-engagement focuses on positive coping (e.g., journaling) rather than digging into pain.

## Clinical Handoff
Before deploying to real users, I would flag the following to the clinical and ethics team:
- **Safety Filter Thresholds**: What exactly defines a "high-sensitivity" memory in a clinical context?
- **Recall Accuracy**: How do we handle "false memories" where the AI incorrectly summarizes a user's statement?
- **Frequency of Contact**: What is the clinically appropriate frequency for AI-initiated re-engagement for someone in high distress?
