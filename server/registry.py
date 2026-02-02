# Tool registry - manages available tools and their metadata
from typing import Dict, Callable, Any, Union
from pydantic import ValidationError
from .tools.add_numbers import add_numbers
from .tools.dummy_tool import dummy_tool
from .schemas.tool_schema import AddNumbersRequest, DummyToolRequest, ToolResponse, ErrorResponse

class ToolNotFoundError(Exception):
    """Raised when a requested tool is not found"""
    pass

class ToolExecutionError(Exception):
    """Raised when tool execution fails"""
    pass

class ToolRegistry:
    """Registry for managing MCP tools"""
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools with their metadata"""
        
        # Register add_numbers tool
        self._tools["add_numbers"] = {
            "function": add_numbers,
            "request_model": AddNumbersRequest,
            "description": "Adds two integers together",
            "parameters": {
                "a": {"type": "integer", "description": "First number"},
                "b": {"type": "integer", "description": "Second number"}
            }
        }
        
        # Register dummy_tool
        self._tools["dummy_tool"] = {
            "function": dummy_tool,
            "request_model": DummyToolRequest,
            "description": "A dummy tool for testing server functionality",
            "parameters": {}
        }
    
    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """Get tool metadata by name"""
        return self._tools.get(tool_name)
    
    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered tools"""
        return self._tools.copy()
    
    def tool_exists(self, tool_name: str) -> bool:
        """Check if a tool exists in the registry"""
        return tool_name in self._tools
    
    def execute_tool(self, tool_name: str, request_data: dict) -> Union[ToolResponse, ErrorResponse]:
        """
        Execute a tool with the given request data
        
        Args:
            tool_name: Name of the tool to execute
            request_data: Dictionary containing tool parameters
            
        Returns:
            ToolResponse on success, ErrorResponse on failure
        """
        # Check if tool exists
        if not self.tool_exists(tool_name):
            return ErrorResponse(
                error=f"Tool '{tool_name}' not found",
                error_type="TOOL_NOT_FOUND",
                details={"available_tools": list(self._tools.keys())}
            )
        
        tool = self.get_tool(tool_name)
        
        try:
            # Validate request data against tool's schema
            request_obj = tool["request_model"](**request_data)
            
            # Execute the tool function
            result = tool["function"](request_obj)
            
            # Ensure result is a ToolResponse
            if not isinstance(result, ToolResponse):
                return ErrorResponse(
                    error="Tool returned invalid response format",
                    error_type="INVALID_RESPONSE",
                    details={"tool_name": tool_name}
                )
            
            return result
            
        except ValidationError as e:
            return ErrorResponse(
                error="Invalid input parameters",
                error_type="VALIDATION_ERROR",
                details={
                    "validation_errors": [
                        {"field": err["loc"][-1], "message": err["msg"]} 
                        for err in e.errors()
                    ],
                    "expected_parameters": tool["parameters"]
                }
            )
        except Exception as e:
            return ErrorResponse(
                error=f"Tool execution failed: {str(e)}",
                error_type="EXECUTION_ERROR",
                details={"tool_name": tool_name}
            )

# Global registry instance
registry = ToolRegistry()