"""Chat database models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Conversation(Base):
    """Conversation model."""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Message model."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    provider = Column(String(50), nullable=True)  # 'groq' or 'gemini'
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")