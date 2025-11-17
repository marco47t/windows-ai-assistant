"""Tool manager with registry integration."""

import time
from typing import Dict, List
from core.logger import logger
from tools.web_search import search_web, format_search_results
from tools.web_navigator import scrape_webpage
from tools.web_processor import search_and_read, format_search_and_read_results
from tools.tool_registry import registry


class ToolManager:
    """Manages and registers tools."""
    
    def __init__(self):
        """Initialize and register all tools."""
        self.last_search_time = 0
        self._register_all_tools()
        logger.info("Tool manager initialized")
    
    def _register_all_tools(self):
        """Register all available tools."""
        
        # Tool 1: Quick web search
        registry.register(
            name="web_search",
            description="Search the web and return links with snippets. Use for quick searches when user just wants links.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5)"
                    }
                },
                "required": ["query"]
            },
            function=self.web_search,
            examples=[
                "web_search(query=\"Python tutorials\")",
                "web_search(query=\"latest AI news\", max_results=3)"
            ]
        )
        
        # Tool 2: Read webpage
        registry.register(
            name="read_webpage",
            description="Read and extract content from a specific webpage URL.",
            parameters={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to read"
                    }
                },
                "required": ["url"]
            },
            function=self.read_webpage,
            examples=[
                "read_webpage(url=\"https://python.org\")"
            ]
        )
        
        # Tool 3: Smart search (search + read multiple results)
        registry.register(
            name="search_and_read",
            description="Intelligent search that searches the web AND reads top results. Returns comprehensive information from multiple sources. Use for research, current events, or when detailed answers are needed.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of pages to read (1-5, default: 3)"
                    }
                },
                "required": ["query"]
            },
            function=self.smart_search,
            examples=[
                "search_and_read(query=\"latest AI developments\")",
                "search_and_read(query=\"Python best practices\", num_results=5)"
            ]
        )
    
    def web_search(self, query: str, max_results: int = 5) -> str:
        """Quick web search."""
        self._rate_limit()
        logger.info(f"Tool: web_search({query})")
        results = search_web(query, max_results)
        return format_search_results(results)
    
    def read_webpage(self, url: str) -> str:
        """Read webpage."""
        logger.info(f"Tool: read_webpage({url})")
        result = scrape_webpage(url)
        
        if result['error']:
            return f"Error: {result['error']}"
        
        return f"**{url}**\n\n{result['text'][:2000]}\n\nFound {len(result['links'])} links."
    
    def smart_search(self, query: str, num_results: int = 3) -> str:
        """Smart search with reading."""
        self._rate_limit()
        logger.info(f"Tool: smart_search({query}, num_results={num_results})")
        
        num_results = min(num_results, 5)
        result = search_and_read(query, num_results=num_results)
        return format_search_and_read_results(result)
    
    def _rate_limit(self):
        """Enforce rate limiting between searches."""
        time_since_last = time.time() - self.last_search_time
        if time_since_last < 2:
            time.sleep(2 - time_since_last)
        self.last_search_time = time.time()
