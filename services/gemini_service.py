"""Google Gemini AI service."""

from typing import List, Dict
import google.generativeai as genai
from core.config import settings
from core.logger import logger
from services.ai_provider import AIProvider


class GeminiService(AIProvider):
    """Gemini AI provider implementation."""
    
    def __init__(self):
        """Initialize Gemini client."""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        logger.info(f"Initialized Gemini service with model: {settings.GEMINI_MODEL}")
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send chat messages to Gemini and get response."""
        try:
            # Convert messages to Gemini format
            chat_history = []
            for msg in messages[:-1]:  # All except last
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })
            
            # Start chat with history
            chat = self.model.start_chat(history=chat_history)
            
            # Send last message
            response = chat.send_message(messages[-1]["content"])
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        # Rough estimate: 1 token ≈ 0.75 words
        return int(len(text.split()) / 0.75)
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "gemini"