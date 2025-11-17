"""Intelligent tool execution with AI decision making."""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from core.logger import logger
from tools.tool_registry import registry


class ToolExecutor:
    """Executes tools based on AI decisions."""
    
    def __init__(self):
        """Initialize executor."""
        self.execution_history: List[Dict] = []
    
    def parse_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse tool call from AI response.
        
        Expected format:
        TOOL_CALL: tool_name(param1="value1", param2="value2")
        
        Args:
            text: AI response text
            
        Returns:
            Dict with tool_name and parameters, or None
        """
        # Look for TOOL_CALL marker
        pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if not match:
            return None
        
        tool_name = match.group(1)
        params_str = match.group(2)
        
        # Parse parameters
        parameters = {}
        if params_str.strip():
            # Simple parameter parsing
            param_pattern = r'(\w+)=(["\'])(.*?)\2'
            for param_match in re.finditer(param_pattern, params_str):
                param_name = param_match.group(1)
                param_value = param_match.group(3)
                parameters[param_name] = param_value
        
        return {
            "tool_name": tool_name,
            "parameters": parameters
        }
    
    def execute_from_text(self, text: str) -> Tuple[Optional[str], bool]:
        """Execute tool if found in text.
        
        Args:
            text: AI response text
            
        Returns:
            Tuple of (tool_result, tool_was_called)
        """
        tool_call = self.parse_tool_call(text)
        
        if not tool_call:
            return None, False
        
        try:
            result = registry.execute_tool(
                tool_call["tool_name"],
                **tool_call["parameters"]
            )
            
            # Log execution
            self.execution_history.append({
                "tool": tool_call["tool_name"],
                "parameters": tool_call["parameters"],
                "result": str(result)[:200]  # First 200 chars
            })
            
            return result, True
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return f"Error: {str(e)}", False
    
    def should_use_tool(self, user_message: str, conversation_history: List[Dict]) -> Optional[str]:
        """Determine if a tool should be used.
        
        Args:
            user_message: User's message
            conversation_history: Chat history
            
        Returns:
            Tool suggestion or None
        """
        # Keywords that suggest tool usage
        tool_triggers = {
            "search_and_read": [
                "latest", "current", "recent", "news", "today",
                "search for", "find information", "what's happening",
                "who is", "what is", "when did"
            ],
            "web_search": [
                "quick search", "find links", "search"
            ],
            "read_webpage": [
                "read this url", "open", "visit"
            ]
        }
        
        message_lower = user_message.lower()
        
        for tool_name, keywords in tool_triggers.items():
            if any(keyword in message_lower for keyword in keywords):
                return tool_name
        
        return None


# Global executor instance
executor = ToolExecutor()
