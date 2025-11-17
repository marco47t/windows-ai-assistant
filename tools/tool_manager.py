"""Enhanced tool manager with system control and code execution."""

import time
from typing import Dict, List
from core.logger import logger
from tools.web_search import search_web, format_search_results
from tools.web_navigator import scrape_webpage
from tools.web_processor import search_and_read, format_search_and_read_results
from tools.system_control import system_controller
from tools.code_executor import code_executor
from tools.tool_registry import registry


class ToolManager:
    """Manages all tools including system control and code execution."""
    
    def __init__(self):
        """Initialize and register all tools."""
        self.last_search_time = 0
        self._register_all_tools()
        logger.info("Enhanced tool manager initialized")
    
    def _register_all_tools(self):
        """Register all available tools."""
        
        # Web search tools (already registered in previous version)
        registry.register(
            name="web_search",
            description="Search the web quickly",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Max results (default 5)"}
                },
                "required": ["query"]
            },
            function=self.web_search,
            examples=["web_search(query=\"Python tutorials\")"]
        )
        
        registry.register(
            name="read_webpage",
            description="Read content from a URL",
            parameters={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to read"}
                },
                "required": ["url"]
            },
            function=self.read_webpage
        )
        
        registry.register(
            name="search_and_read",
            description="Search and read top results (comprehensive)",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "description": "Results to read (1-5)"}
                },
                "required": ["query"]
            },
            function=self.smart_search
        )
        
        # System control tools (NEW)
        registry.register(
            name="open_app",
            description="Open an application on Windows",
            parameters={
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Application name (chrome, notepad, calculator, etc.)"},
                    "args": {"type": "string", "description": "Optional arguments"}
                },
                "required": ["app_name"]
            },
            function=self.open_app,
            examples=["open_app(app_name=\"chrome\")", "open_app(app_name=\"notepad\")"]
        )
        
        registry.register(
            name="create_folder",
            description="Create a folder on the system",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Folder path"}
                },
                "required": ["path"]
            },
            function=self.create_folder,
            examples=["create_folder(path=\"C:\\\\Projects\")"]
        )
        
        registry.register(
            name="take_screenshot",
            description="Take a screenshot",
            parameters={
                "type": "object",
                "properties": {
                    "save_path": {"type": "string", "description": "Optional save path"}
                },
                "required": []
            },
            function=self.take_screenshot
        )
        
        # Code execution tools (NEW)
        registry.register(
            name="execute_code",
            description="Execute Python code safely",
            parameters={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"]
            },
            function=self.execute_code,
            examples=["execute_code(code=\"print(2 + 2)\")"]
        )
        
        registry.register(
            name="calculate",
            description="Evaluate a mathematical expression",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"]
            },
            function=self.calculate,
            examples=["calculate(expression=\"2 ** 10\")"]
        )
    
    # Web tools
    def web_search(self, query: str, max_results: int = 5) -> str:
        """Quick web search."""
        self._rate_limit()
        results = search_web(query, max_results)
        return format_search_results(results)
    
    def read_webpage(self, url: str) -> str:
        """Read webpage."""
        result = scrape_webpage(url)
        if result['error']:
            return f"Error: {result['error']}"
        return f"**{url}**\n\n{result['text'][:2000]}"
    
    def smart_search(self, query: str, num_results: int = 3) -> str:
        """Smart search."""
        self._rate_limit()
        result = search_and_read(query, num_results=min(num_results, 5))
        return format_search_and_read_results(result)
    
    # System control tools
    def open_app(self, app_name: str, args: str = "") -> str:
        """Open application."""
        result = system_controller.open_application(app_name, args)
        return result['message']
    
    def create_folder(self, path: str) -> str:
        """Create folder."""
        result = system_controller.create_folder(path)
        return result['message']
    
    def take_screenshot(self, save_path: str = None) -> str:
        """Take screenshot."""
        result = system_controller.take_screenshot(save_path)
        return result['message']
    
    # Code execution tools
    def execute_code(self, code: str) -> str:
        """Execute Python code."""
        result = code_executor.execute_code(code)
        return code_executor.format_execution_result(result)
    
    def calculate(self, expression: str) -> str:
        """Calculate expression."""
        result = code_executor.execute_expression(expression)
        if result['success']:
            return f"Result: {result['result']}"
        return f"Error: {result['error']}"
    
    def _rate_limit(self):
        """Rate limiting."""
        time_since_last = time.time() - self.last_search_time
        if time_since_last < 2:
            time.sleep(2 - time_since_last)
        self.last_search_time = time.time()
