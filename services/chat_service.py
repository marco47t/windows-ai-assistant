"""Chat service for managing conversations."""

from typing import List, Dict, Tuple
from datetime import datetime
from core.database import SessionLocal
from core.logger import logger
from models.chat import Conversation, Message
from services.router import AIRouter


class ChatService:
    """Service for managing chat conversations."""
    
    def __init__(self, router: AIRouter):
        """Initialize chat service.
        
        Args:
            router: AI provider router
        """
        self.router = router
        self.db = SessionLocal()
        self.current_conversation = None
        self._init_conversation()
    
    def _init_conversation(self):
        """Initialize or get current conversation."""
        # Get or create conversation
        conversation = self.db.query(Conversation).order_by(Conversation.created_at.desc()).first()
        
        if not conversation:
            conversation = Conversation(title="New Chat")
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
        
        self.current_conversation = conversation
        logger.info(f"Using conversation: {conversation.id}")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history.
        
        Returns:
            List of message dicts
        """
        messages = self.db.query(Message).filter(
            Message.conversation_id == self.current_conversation.id
        ).order_by(Message.timestamp).all()
        
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]
    
    def send_message(self, content: str) -> Tuple[str, str]:
        """Send a message and get AI response.
        
        Args:
            content: User message
            
        Returns:
            Tuple of (response, provider_name)
        """
        # Save user message
        user_msg = Message(
            conversation_id=self.current_conversation.id,
            role="user",
            content=content
        )
        self.db.add(user_msg)
        self.db.commit()
        
        # Get conversation history
        history = self.get_history()
        
        # Get AI response
        response, provider = self.router.chat(history)
        
        # Save assistant message
        ai_msg = Message(
            conversation_id=self.current_conversation.id,
            role="assistant",
            content=response,
            provider=provider
        )
        self.db.add(ai_msg)
        
        # Update conversation timestamp
        self.current_conversation.updated_at = datetime.utcnow()
        self.db.commit()
        
        return response, provider
    
    def clear_history(self):
        """Clear current conversation and start new one."""
        # Create new conversation
        conversation = Conversation(title="New Chat")
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        self.current_conversation = conversation
        logger.info("Started new conversation")
    
    def __del__(self):
        """Cleanup."""
        if hasattr(self, 'db'):
            self.db.close()