# FastAPI MCP test server - main entry point
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Union
import uvicorn

from .config import config
from .registry import registry
from .schemas.tool_schema import HealthResponse, ToolResponse, ErrorResponse

# Create FastAPI app instance
app = FastAPI(
    title="MCP Test Server",
    description="A minimal MCP-style server for testing and validation",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for consistent error responses"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "error_type": "INTERNAL_ERROR",
            "details": {"message": str(exc)}
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify server is running"""
    return HealthResponse(
        status="healthy",
        message="MCP test server is operational"
    )

@app.get(f"{config.API_PREFIX}/tools")
async def list_tools():
    """List all available tools with their descriptions"""
    try:
        tools = registry.list_tools()
        
        # Format tools for API response
        formatted_tools = {}
        for name, tool_info in tools.items():
            formatted_tools[name] = {
                "description": tool_info["description"],
                "parameters": tool_info["parameters"]
            }
        
        return {
            "success": True,
            "tools": formatted_tools,
            "count": len(formatted_tools)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Failed to list tools: {str(e)}",
                "error_type": "INTERNAL_ERROR"
            }
        )

@app.post(f"{config.API_PREFIX}/tools/add_numbers")
async def call_add_numbers(request: Dict[str, Any]) -> Union[ToolResponse, ErrorResponse]:
    """Execute the add_numbers tool"""
    result = registry.execute_tool("add_numbers", request)
    
    # Return error response with appropriate HTTP status
    if isinstance(result, ErrorResponse):
        status_code = 400 if result.error_type == "VALIDATION_ERROR" else 500
        return JSONResponse(status_code=status_code, content=result.dict())
    
    return result

@app.post(f"{config.API_PREFIX}/tools/dummy_tool")
async def call_dummy_tool() -> Union[ToolResponse, ErrorResponse]:
    """Execute the dummy_tool"""
    result = registry.execute_tool("dummy_tool", {})
    
    # Return error response with appropriate HTTP status
    if isinstance(result, ErrorResponse):
        return JSONResponse(status_code=500, content=result.dict())
    
    return result

@app.post(f"{config.API_PREFIX}/tools/{{tool_name}}")
async def call_generic_tool(tool_name: str, request: Dict[str, Any] = None):
    """Generic endpoint for calling any tool by name"""
    if request is None:
        request = {}
    
    result = registry.execute_tool(tool_name, request)
    
    # Return error response with appropriate HTTP status
    if isinstance(result, ErrorResponse):
        if result.error_type == "TOOL_NOT_FOUND":
            status_code = 404
        elif result.error_type == "VALIDATION_ERROR":
            status_code = 400
        else:
            status_code = 500
        
        return JSONResponse(status_code=status_code, content=result.dict())
    
    return result

@app.get("/")
async def root():
    """Root endpoint with basic server info"""
    return {
        "message": "MCP Test Server",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health_check": "/health",
            "api_docs": "/docs",
            "list_tools": f"{config.API_PREFIX}/tools",
            "add_numbers": f"{config.API_PREFIX}/tools/add_numbers",
            "dummy_tool": f"{config.API_PREFIX}/tools/dummy_tool"
        }
    }

if __name__ == "__main__":
    # Run the server when executed directly
    uvicorn.run(
        "server.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )