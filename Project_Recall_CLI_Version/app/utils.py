import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def generate_id(prefix: str = "") -> str:
    return f"{prefix}{str(uuid.uuid4())[:8]}"

def get_now() -> datetime:
    return datetime.utcnow()

def is_mock_mode() -> bool:
    return os.getenv("MOCK_LLM", "false").lower() == "true"

def get_env_var(name: str, default: str = None) -> str:
    return os.getenv(name, default)
