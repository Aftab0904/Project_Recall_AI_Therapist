import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM Provider Configuration
    LLM_PROVIDER: str = "mock"  # ollama | openrouter | mock
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "deepseek-r1:7b"
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "deepseek/deepseek-r1"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./mentra_memory.db"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # Application Environment
    APP_ENV: str = "development"

settings = Settings()
