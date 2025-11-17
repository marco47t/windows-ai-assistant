"""Tool manager with intelligent web search."""

from typing import Dict, Any, List
from core.logger import logger
from tools.web_search import search_web, format_search_results
from tools.web_navigator import scrape_webpage
from tools.web_processor import search_and_read, format_search_and_read_results


class ToolManager:
    """Manages available tools for the AI."""
    
    def __init__(self):
        """Initialize tool manager."""
        self.tools = {
            'web_search': self.web_search,
            'read_webpage': self.read_webpage,
            'search_and_read': self.smart_search,  # NEW: Intelligent search
        }
    
    def web_search(self, query: str, max_results: int = 5) -> str:
        """Quick web search (links only).
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Formatted search results
        """
        logger.info(f"Tool: web_search({query})")
        results = search_web(query, max_results)
        return format_search_results(results)
    
    def read_webpage(self, url: str) -> str:
        """Read and extract text from a webpage.
        
        Args:
            url: URL to read
            
        Returns:
            Webpage content
        """
        logger.info(f"Tool: read_webpage({url})")
        result = scrape_webpage(url)
        
        if result['error']:
            return f"Error: {result['error']}"
        
        output = [
            f"**{url}**",
            "",
            result['text'][:2000],
            "",
            f"Found {len(result['links'])} links on this page."
        ]
        
        return "\n".join(output)
    
    def smart_search(self, query: str, num_results: int = 3) -> str:
        """Intelligent search: searches AND reads top results.
        
        Args:
            query: Search query
            num_results: Number of pages to read (1-5)
            
        Returns:
            Comprehensive search results with page contents
        """
        logger.info(f"Tool: smart_search({query}, num_results={num_results})")
        
        # Limit to 5 results max to avoid rate limits
        num_results = min(num_results, 5)
        
        result = search_and_read(query, num_results=num_results)
        return format_search_and_read_results(result)
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a tool by name.
        
        Args:
            tool_name: Name of the tool
            **kwargs: Tool arguments
            
        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            return f"Error: Unknown tool '{tool_name}'"
        
        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            logger.error(f"Tool error: {e}")
            return f"Error executing tool: {str(e)}"
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools.
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> str:
        """Get descriptions of all tools.
        
        Returns:
            Formatted tool descriptions
        """
        descriptions = """
**Available Tools:**

1. **web_search(query, max_results=5)**
   - Quick web search returning links and snippets
   - Use when user just wants links
   
2. **read_webpage(url)**
   - Read and extract content from a specific URL
   - Use when user provides a URL to read
   
3. **search_and_read(query, num_results=3)**
   - Intelligent search: searches web AND reads top results
   - Returns comprehensive information from multiple sources
   - Use when user needs in-depth information on a topic
   - Best for: research, current events, detailed answers
"""
        return descriptions
