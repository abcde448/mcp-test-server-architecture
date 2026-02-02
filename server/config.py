# Basic configuration for MCP test server
import os

class Config:
    """Simple configuration class for the MCP server"""
    
    # Server settings
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    # API settings
    API_PREFIX = "/api/v1"
    
config = Config()