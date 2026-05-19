import re
import hashlib
from datetime import datetime

def normalize_text(text: str) -> str:
    """Lowercase and remove non-alphanumeric characters for comparison."""
    if not text:
        return ""
    return re.sub(r'[^a-z0-9]', '', text.lower())

def generate_fingerprint(user_id: str, memory_type: str, summary: str) -> str:
    """Generate a unique fingerprint for memory deduplication."""
    norm_summary = normalize_text(summary)
    raw = f"{user_id}|{memory_type}|{norm_summary}"
    return hashlib.sha256(raw.encode()).hexdigest()

def get_current_timestamp() -> datetime:
    return datetime.utcnow()

def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
