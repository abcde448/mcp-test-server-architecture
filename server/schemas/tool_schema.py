# Pydantic schemas for tool requests and responses
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class ToolRequest(BaseModel):
    """Base request model for tool calls"""
    pass

class AddNumbersRequest(ToolRequest):
    """Request schema for add_numbers tool"""
    a: int = Field(..., description="First integer to add")
    b: int = Field(..., description="Second integer to add")

class DummyToolRequest(ToolRequest):
    """Request schema for dummy_tool (no parameters needed)"""
    pass

class ToolResponse(BaseModel):
    """Standard response model for all tools"""
    success: bool
    result: Optional[Any] = None
    message: str = ""
    error_type: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    error_type: str
    details: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str