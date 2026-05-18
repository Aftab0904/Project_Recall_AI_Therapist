# API Examples

## 1. Ingest Sample Data
**POST** `/api/ingest`
**Response**:
```json
{
  "session_count": 5,
  "memories_extracted": 12,
  "summary": [
    "User shared feeling overwhelmed by work boundaries.",
    "User mentioned trouble sleeping due to work ruminations.",
    ...
  ]
}
```

## 2. Start Session (Get Warm Opener)
**POST** `/api/session/start`
**Body**:
```json
{
  "user_id": "demo_user",
  "current_message": "Hey, I'm feeling a bit better today."
}
```
**Response**:
```json
{
  "message": "Welcome back! I'm glad to hear you're feeling a bit better. I remember we were talking about your progress with setting work boundaries last time. How has that been feeling for you since then?",
  "memories_used": ["Boundary Progress"],
  "safety_notes": null
}
```

## 3. View Memories
**GET** `/api/memories/demo_user`
**Response**:
```json
[
  {
    "id": "uuid-123",
    "theme": "Work-Life Balance",
    "summary": "User shared feeling overwhelmed by work boundaries.",
    "importance": 8,
    "status": "active",
    ...
  }
]
```

## 4. Trigger Notification
**POST** `/api/notifications/trigger`
**Body**:
```json
{
  "user_id": "demo_user"
}
```
**Response**:
```json
{
  "should_send": true,
  "scenario": "work_anxiety_checkin",
  "reason": "User has been away for 3 days with unresolved work anxiety.",
  "copy": "Hi there. I was thinking about our last talk about work. It seemed like a lot was on your mind. Just wanted to see how you're feeling today?"
}
```
