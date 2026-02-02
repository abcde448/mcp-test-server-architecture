# Dummy tool for testing and validation
from ..schemas.tool_schema import DummyToolRequest, ToolResponse
import time

def dummy_tool(request: DummyToolRequest) -> ToolResponse:
    """
    A simple dummy tool that returns a test message
    Useful for validating the MCP server is working correctly
    
    Args:
        request: DummyToolRequest (no parameters needed)
        
    Returns:
        ToolResponse with a test message
    """
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        return ToolResponse(
            success=True,
            result={
                "timestamp": timestamp, 
                "status": "operational",
                "server_info": "MCP Test Server v1.0.0"
            },
            message="Dummy tool executed successfully"
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            result=None,
            message=f"Error in dummy tool: {str(e)}",
            error_type="EXECUTION_ERROR"
        )