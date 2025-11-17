"""Intelligent AI provider routing."""

from typing import List, Dict, Tuple
from core.config import settings
from core.logger import logger
from services.groq_service import GroqService
from services.gemini_service import GeminiService


class AIRouter:
    """Smart router for AI providers."""
    
    def __init__(self):
        """Initialize router with providers."""
        self.providers = {}
        self.current_provider = settings.DEFAULT_PROVIDER
        
        # Initialize Groq (required)
        try:
            self.providers["groq"] = GroqService()
            logger.info("Groq provider initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            raise
        
        # Initialize Gemini (optional)
        try:
            self.providers["gemini"] = GeminiService()
            logger.info("Gemini provider initialized")
        except Exception as e:
            logger.warning(f"Gemini not available: {e}")
    
    def set_provider(self, provider: str):
        """Manually set provider.
        
        Args:
            provider: 'groq', 'gemini', or 'auto'
        """
        if provider not in ["groq", "gemini", "auto"]:
            raise ValueError(f"Invalid provider: {provider}")
        
        if provider != "auto" and provider not in self.providers:
            raise ValueError(f"Provider {provider} not available")
        
        self.current_provider = provider
        logger.info(f"Provider set to: {provider}")
    
    def select_provider(self, messages: List[Dict[str, str]]) -> str:
        """Intelligently select provider based on task.
        
        Args:
            messages: Chat messages
            
        Returns:
            Provider name ('groq' or 'gemini')
        """
        # Manual override
        if self.current_provider != "auto":
            return self.current_provider
        
        # Estimate total tokens
        total_text = " ".join([msg["content"] for msg in messages])
        estimated_tokens = self.providers["groq"].estimate_tokens(total_text)
        
        # Route based on token count
        if estimated_tokens > settings.ROUTING_TOKEN_THRESHOLD:
            # Use Gemini for large context
            if "gemini" in self.providers:
                logger.info(f"Routing to Gemini (tokens: {estimated_tokens})")
                return "gemini"
        
        # Default to Groq for speed
        logger.info(f"Routing to Groq (tokens: {estimated_tokens})")
        return "groq"
    
    def chat(self, messages: List[Dict[str, str]]) -> Tuple[str, str]:
        """Send chat messages using selected provider.
        
        Args:
            messages: Chat messages
            
        Returns:
            Tuple of (response, provider_name)
        """
        provider_name = self.select_provider(messages)
        provider = self.providers[provider_name]
        
        try:
            response = provider.chat(messages)
            return response, provider_name
        except Exception as e:
            logger.error(f"Error with {provider_name}: {e}")
            
            # Fallback to other provider
            fallback = "gemini" if provider_name == "groq" else "groq"
            if fallback in self.providers:
                logger.info(f"Falling back to {fallback}")
                response = self.providers[fallback].chat(messages)
                return response, fallback
            
            raise