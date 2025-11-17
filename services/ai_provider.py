"""AI Provider interface."""

from abc import ABC, abstractmethod
from typing import List, Dict


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send chat messages and get response.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            AI response string
        """
        pass
    
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text.
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        pass