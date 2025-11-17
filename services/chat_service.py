"""Chat service with tool calling and memory."""

from typing import List, Dict, Tuple
from datetime import datetime
from core.database import SessionLocal
from core.logger import logger
from models.chat import Conversation, Message
from services.router import AIRouter
from tools.tool_manager import ToolManager
from tools.tool_registry import registry
from services.tool_executor import executor
from services.memory_service import memory_store
from services.synthesis_service import synthesis_service
import re


class ChatService:
    """Enhanced chat service with intelligence."""
    
    def __init__(self, router: AIRouter):
        """Initialize chat service."""
        self.router = router
        self.tool_manager = ToolManager()
        self.db = SessionLocal()
        self.current_conversation = None
        self._init_conversation()
    
    def _init_conversation(self):
        """Initialize conversation."""
        conversation = self.db.query(Conversation).order_by(
            Conversation.created_at.desc()
        ).first()
        
        if not conversation:
            conversation = Conversation(title="New Chat")
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
        
        self.current_conversation = conversation
        logger.info(f"Using conversation: {conversation.id}")
    
    def _should_use_tool(self, message: str) -> bool:
        """Determine if message requires tools."""
        tool_keywords = [
            'latest', 'current', 'recent', 'news', 'search',
            'find', 'look up', 'who is', 'what is', 'when',
            'read', 'visit', 'open'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in tool_keywords)
    
    def _build_context_with_memory(self, user_message: str) -> str:
        """Enhance message with relevant memories.
        
        Args:
            user_message: User's message
            
        Returns:
            Enhanced message with memory context
        """
        # Search relevant memories
        relevant_memories = memory_store.search_memories(user_message, limit=3)
        
        if not relevant_memories:
            return user_message
        
        # Add memory context
        memory_context = "\n\n**Relevant Information from Memory:**\n"
        for memory in relevant_memories:
            memory_context += f"- {memory['content']}\n"
        
        return user_message + memory_context
    
    def _extract_important_facts(self, conversation: List[Dict]) -> List[str]:
        """Extract important facts to remember.
        
        Args:
            conversation: Conversation history
            
        Returns:
            List of facts
        """
        facts = []
        
        # Simple extraction: look for statements of fact
        fact_patterns = [
            r"(?:remember|note|important):\s*(.+)",
            r"my\s+(?:name|email|phone|address)\s+is\s+(.+)",
            r"I\s+(?:like|prefer|hate|love)\s+(.+)"
        ]
        
        for msg in conversation:
            if msg['role'] == 'user':
                content = msg['content']
                for pattern in fact_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    facts.extend(matches)
        
        return facts
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        messages = self.db.query(Message).filter(
            Message.conversation_id == self.current_conversation.id
        ).order_by(Message.timestamp).all()
        
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    def send_message(
        self,
        content: str,
        use_tools: bool = True,
        use_memory: bool = True
    ) -> Tuple[str, str]:
        """Send message with intelligent tool use and memory.
        
        Args:
            content: User message
            use_tools: Enable automatic tool use
            use_memory: Enable memory retrieval
            
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
        
        # Enhance with memory
        enhanced_content = content
        if use_memory:
            enhanced_content = self._build_context_with_memory(content)
        
        # Check if tools needed
        tool_result = None
        if use_tools and self._should_use_tool(content):
            suggested_tool = executor.should_use_tool(content, [])
            
            if suggested_tool == "search_and_read":
                logger.info("Auto-triggering search_and_read")
                query = content
                tool_result = self.tool_manager.smart_search(query, num_results=3)
                
                # Add tool result to context
                enhanced_content = f"""{content}

**Web Search Results:**
{tool_result}

Please provide a comprehensive answer with citations [1], [2], [3] etc."""
        
        # Get conversation history
        history = self.get_history()
        history[-1]['content'] = enhanced_content
        
        # Add tool descriptions to system context
        system_message = {
            "role": "system",
            "content": f"""You are a helpful AI assistant with access to tools.

{registry.format_tools_for_prompt()}

When answering questions:
1. Use information from web search results when provided
2. Cite sources using [1], [2], [3] format
3. Be comprehensive and accurate
4. If information seems contradictory, mention it
"""
        }
        
        history = [system_message] + history
        
        # Get AI response
        response, provider = self.router.chat(history)
        
        # Extract and save important facts to memory
        facts = self._extract_important_facts(history)
        for fact in facts:
            memory_store.add_memory(
                content=fact,
                memory_type="fact",
                tags=["conversation"],
                metadata={"conversation_id": self.current_conversation.id}
            )
        
        # Save assistant message
        ai_msg = Message(
            conversation_id=self.current_conversation.id,
            role="assistant",
            content=response,
            provider=provider
        )
        self.db.add(ai_msg)
        
        self.current_conversation.updated_at = datetime.utcnow()
        self.db.commit()
        
        return response, provider
    
    def clear_history(self):
        """Clear conversation."""
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
