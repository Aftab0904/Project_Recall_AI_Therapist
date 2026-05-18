import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum as SQLEnum, Text
from .config import settings
from .models import MemoryType, SensitivityLevel, MemoryStatus
from datetime import datetime

Base = declarative_base()

class MemoryDB(Base):
    __tablename__ = "memories"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    source_session_id = Column(String, nullable=True)
    memory_type = Column(SQLEnum(MemoryType))
    theme = Column(String)
    summary = Column(Text)
    emotional_tone = Column(String)
    status = Column(SQLEnum(MemoryStatus), default=MemoryStatus.ACTIVE)
    importance = Column(Integer)
    sensitivity = Column(SQLEnum(SensitivityLevel))
    safe_to_reference = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_mentioned_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

class SessionDB(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime)
    theme = Column(String)
    emotional_tone = Column(String)
    raw_transcript = Column(Text, nullable=True)

class NotificationEventDB(Base):
    __tablename__ = "notification_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    scenario = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    copy_sent = Column(Text)

class ExclusionItemDB(Base):
    __tablename__ = "exclusion_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
