# Add numbers tool - simple arithmetic operation
from ..schemas.tool_schema import AddNumbersRequest, ToolResponse

def add_numbers(request: AddNumbersRequest) -> ToolResponse:
    """
    Adds two integers together
    
    Args:
        request: AddNumbersRequest containing a and b integers
        
    Returns:
        ToolResponse with the sum result
    """
    try:
        # Validate inputs are within reasonable range
        if abs(request.a) > 1_000_000 or abs(request.b) > 1_000_000:
            return ToolResponse(
                success=False,
                result=None,
                message="Numbers too large (max absolute value: 1,000,000)",
                error_type="VALUE_ERROR"
            )
        
        result = request.a + request.b
        return ToolResponse(
            success=True,
            result=result,
            message=f"Successfully added {request.a} + {request.b} = {result}"
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            result=None,
            message=f"Error adding numbers: {str(e)}",
            error_type="EXECUTION_ERROR"
        )