"""Tool registry with JSON schema definitions."""

from typing import Dict, List, Any, Callable
from core.logger import logger


class Tool:
    """Tool definition."""
    
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        function: Callable,
        examples: List[str] = None
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function
        self.examples = examples or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "examples": self.examples
        }
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool."""
        return self.function(**kwargs)


class ToolRegistry:
    """Registry of available tools."""
    
    def __init__(self):
        """Initialize registry."""
        self.tools: Dict[str, Tool] = {}
        logger.info("Tool registry initialized")
    
    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        function: Callable,
        examples: List[str] = None
    ):
        """Register a new tool.
        
        Args:
            name: Tool name
            description: What the tool does
            parameters: Parameter schema
            function: Function to execute
            examples: Example usage
        """
        tool = Tool(name, description, parameters, function, examples)
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")
    
    def get_tool(self, name: str) -> Tool:
        """Get tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all tool names."""
        return list(self.tools.keys())
    
    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get schema for all tools (for AI context)."""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool by name.
        
        Args:
            name: Tool name
            **kwargs: Tool arguments
            
        Returns:
            Tool result
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")
        
        try:
            logger.info(f"Executing tool: {name} with args: {kwargs}")
            return tool.execute(**kwargs)
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            raise
    
    def format_tools_for_prompt(self) -> str:
        """Format tools for AI prompt."""
        output = ["**Available Tools:**\n"]
        
        for tool in self.tools.values():
            output.append(f"### {tool.name}")
            output.append(f"{tool.description}\n")
            output.append("**Parameters:**")
            
            for param_name, param_info in tool.parameters.get("properties", {}).items():
                param_type = param_info.get("type", "string")
                param_desc = param_info.get("description", "")
                required = param_name in tool.parameters.get("required", [])
                req_marker = " (required)" if required else " (optional)"
                output.append(f"- `{param_name}` ({param_type}){req_marker}: {param_desc}")
            
            if tool.examples:
                output.append("\n**Examples:**")
                for example in tool.examples:
                    output.append(f"- {example}")
            
            output.append("")
        
        return "\n".join(output)


# Global registry instance
registry = ToolRegistry()
