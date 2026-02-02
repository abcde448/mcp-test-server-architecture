#!/usr/bin/env python3
"""
Simple script to run the MCP test server
Usage: python run_server.py
"""

import uvicorn
from server.main import app
from server.config import config

if __name__ == "__main__":
    print(f"Starting MCP Test Server on {config.HOST}:{config.PORT}")
    print(f"API Documentation: http://{config.HOST}:{config.PORT}/docs")
    print(f"Health Check: http://{config.HOST}:{config.PORT}/health")
    
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )