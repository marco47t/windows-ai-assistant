"""Chat service with intelligent tool usage."""

from typing import List, Dict, Tuple
from datetime import datetime
from core.database import SessionLocal
from core.logger import logger
from models.chat import Conversation, Message
from services.router import AIRouter
from tools.tool_manager import ToolManager
import re


class ChatService:
    """Service for managing chat conversations with intelligent tool use."""
    
    def __init__(self, router: AIRouter):
        """Initialize chat service.
        
        Args:
            router: AI provider router
        """
        self.router = router
        self.tool_manager = ToolManager()
        self.db = SessionLocal()
        self.current_conversation = None
        self._init_conversation()
    
    def _init_conversation(self):
        """Initialize or get current conversation."""
        conversation = self.db.query(Conversation).order_by(Conversation.created_at.desc()).first()
        
        if not conversation:
            conversation = Conversation(title="New Chat")
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
        
        self.current_conversation = conversation
        logger.info(f"Using conversation: {conversation.id}")
    
    def _should_use_web_search(self, message: str) -> bool:
        """Determine if message requires web search.
        
        Args:
            message: User message
            
        Returns:
            True if web search is needed
        """
        # Keywords that suggest web search needed
        web_keywords = [
            'latest', 'current', 'recent', 'news', 'today',
            'search for', 'find information', 'look up',
            'what is happening', 'who is', 'when did',
            'update', '2025', '2024', 'now', 'trending'
        ]
        
        message_lower = message.lower()
        
        # Check for keywords
        return any(keyword in message_lower for keyword in web_keywords)
    
    def _extract_search_query(self, message: str) -> str:
        """Extract search query from user message.
        
        Args:
            message: User message
            
        Returns:
            Cleaned search query
        """
        # Remove command words
        query = message
        patterns = [
            r'(?:search|find|look up|google)\s+(?:for\s+)?',
            r'(?:what|who|when|where|why|how)\s+(?:is|are|was|were|did|does)\s+',
        ]
        
        for pattern in patterns:
            query = re.sub(pattern, '', query, flags=re.IGNORECASE)
        
        return query.strip()
    
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
    
    def send_message(self, content: str, use_smart_search: bool = True) -> Tuple[str, str]:
        """Send a message and get AI response with intelligent tool use.
        
        Args:
            content: User message
            use_smart_search: Enable automatic web search
            
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
        
        # Check if we should search web
        enhanced_content = content
        tool_used = None
        
        if use_smart_search and self._should_use_web_search(content):
            logger.info("Auto-triggering intelligent web search")
            query = self._extract_search_query(content)
            
            # Use smart search (searches AND reads results)
            search_context = self.tool_manager.smart_search(query, num_results=3)
            
            # Enhance the prompt with search results
            enhanced_content = f"""{content}

I've searched the web and read the top results for you. Here's what I found:

{search_context}

Please provide a comprehensive answer based on this information."""
            
            tool_used = "smart_search"
        
        # Get conversation history
        history = self.get_history()
        
        # Replace last message with enhanced version
        if tool_used:
            history[-1]['content'] = enhanced_content
        
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
