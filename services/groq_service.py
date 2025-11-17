"""Groq AI service."""

from typing import List, Dict
from groq import Groq
from core.config import settings
from core.logger import logger
from services.ai_provider import AIProvider


class GroqService(AIProvider):
    """Groq AI provider implementation."""
    
    def __init__(self):
        """Initialize Groq client."""
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        logger.info(f"Initialized Groq service with model: {self.model}")
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send chat messages to Groq and get response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        # Rough estimate: 1 token ≈ 0.75 words
        return int(len(text.split()) / 0.75)
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "groq"