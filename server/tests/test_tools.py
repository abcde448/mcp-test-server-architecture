# Comprehensive tests for MCP tools and server functionality
import pytest
from server.tools.add_numbers import add_numbers
from server.tools.dummy_tool import dummy_tool
from server.schemas.tool_schema import AddNumbersRequest, DummyToolRequest, ToolResponse, ErrorResponse
from server.registry import registry

class TestAddNumbersTool:
    """Test cases for add_numbers tool"""
    
    def test_add_numbers_positive(self):
        """Test add_numbers with positive integers"""
        request = AddNumbersRequest(a=5, b=3)
        response = add_numbers(request)
        
        assert response.success is True
        assert response.result == 8
        assert "5 + 3 = 8" in response.message
        assert response.error_type is None
    
    def test_add_numbers_negative(self):
        """Test add_numbers with negative numbers"""
        request = AddNumbersRequest(a=-5, b=10)
        response = add_numbers(request)
        
        assert response.success is True
        assert response.result == 5
        assert "-5 + 10 = 5" in response.message
    
    def test_add_numbers_zero(self):
        """Test add_numbers with zero"""
        request = AddNumbersRequest(a=0, b=42)
        response = add_numbers(request)
        
        assert response.success is True
        assert response.result == 42
    
    def test_add_numbers_large_values_within_limit(self):
        """Test add_numbers with large but valid values"""
        request = AddNumbersRequest(a=999999, b=-999999)
        response = add_numbers(request)
        
        assert response.success is True
        assert response.result == 0
    
    def test_add_numbers_too_large(self):
        """Test add_numbers with values exceeding limit"""
        request = AddNumbersRequest(a=1000001, b=5)
        response = add_numbers(request)
        
        assert response.success is False
        assert response.result is None
        assert "too large" in response.message.lower()
        assert response.error_type == "VALUE_ERROR"

class TestDummyTool:
    """Test cases for dummy_tool"""
    
    def test_dummy_tool_success(self):
        """Test dummy_tool execution"""
        request = DummyToolRequest()
        response = dummy_tool(request)
        
        assert response.success is True
        assert isinstance(response.result, dict)
        assert "timestamp" in response.result
        assert "status" in response.result
        assert "server_info" in response.result
        assert response.result["status"] == "operational"
        assert "MCP Test Server" in response.result["server_info"]
        assert response.message == "Dummy tool executed successfully"
        assert response.error_type is None

class TestToolRegistry:
    """Test cases for tool registry functionality"""
    
    def test_registry_list_tools(self):
        """Test listing all available tools"""
        tools = registry.list_tools()
        
        assert isinstance(tools, dict)
        assert "add_numbers" in tools
        assert "dummy_tool" in tools
        assert len(tools) == 2
    
    def test_registry_tool_exists(self):
        """Test tool existence checking"""
        assert registry.tool_exists("add_numbers") is True
        assert registry.tool_exists("dummy_tool") is True
        assert registry.tool_exists("nonexistent_tool") is False
    
    def test_registry_get_tool(self):
        """Test getting tool metadata"""
        tool = registry.get_tool("add_numbers")
        
        assert tool is not None
        assert "function" in tool
        assert "request_model" in tool
        assert "description" in tool
        assert "parameters" in tool
        assert tool["description"] == "Adds two integers together"
    
    def test_registry_execute_valid_tool(self):
        """Test executing a valid tool with valid data"""
        result = registry.execute_tool("add_numbers", {"a": 10, "b": 20})
        
        assert isinstance(result, ToolResponse)
        assert result.success is True
        assert result.result == 30
    
    def test_registry_execute_invalid_tool_name(self):
        """Test executing a non-existent tool"""
        result = registry.execute_tool("invalid_tool", {})
        
        assert isinstance(result, ErrorResponse)
        assert result.success is False
        assert result.error_type == "TOOL_NOT_FOUND"
        assert "invalid_tool" in result.error
        assert "available_tools" in result.details
    
    def test_registry_execute_invalid_parameters(self):
        """Test executing a tool with invalid parameters"""
        result = registry.execute_tool("add_numbers", {"a": "not_a_number", "b": 5})
        
        assert isinstance(result, ErrorResponse)
        assert result.success is False
        assert result.error_type == "VALIDATION_ERROR"
        assert "Invalid input parameters" in result.error
        assert "validation_errors" in result.details
    
    def test_registry_execute_missing_parameters(self):
        """Test executing a tool with missing required parameters"""
        result = registry.execute_tool("add_numbers", {"a": 5})  # Missing 'b'
        
        assert isinstance(result, ErrorResponse)
        assert result.success is False
        assert result.error_type == "VALIDATION_ERROR"
        assert "validation_errors" in result.details
    
    def test_registry_execute_extra_parameters(self):
        """Test executing a tool with extra parameters (should be ignored)"""
        result = registry.execute_tool("add_numbers", {"a": 5, "b": 3, "extra": "ignored"})
        
        assert isinstance(result, ToolResponse)
        assert result.success is True
        assert result.result == 8
    
    def test_registry_execute_dummy_tool_empty_params(self):
        """Test executing dummy_tool with empty parameters"""
        result = registry.execute_tool("dummy_tool", {})
        
        assert isinstance(result, ToolResponse)
        assert result.success is True
        assert "timestamp" in result.result

class TestResponseFormats:
    """Test response format consistency"""
    
    def test_tool_response_structure(self):
        """Test ToolResponse has correct structure"""
        response = ToolResponse(success=True, result=42, message="test")
        
        assert hasattr(response, 'success')
        assert hasattr(response, 'result')
        assert hasattr(response, 'message')
        assert hasattr(response, 'error_type')
    
    def test_error_response_structure(self):
        """Test ErrorResponse has correct structure"""
        response = ErrorResponse(error="test error", error_type="TEST_ERROR")
        
        assert hasattr(response, 'success')
        assert hasattr(response, 'error')
        assert hasattr(response, 'error_type')
        assert hasattr(response, 'details')
        assert response.success is False