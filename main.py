#!/usr/bin/env python3
"""
SudarshanChakraAI - Main Entry Point
Redirects to backend/main.py for Railway deployment
"""

import os
import sys
import subprocess

def main():
    """Main entry point that redirects to backend"""
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Add backend to Python path
    sys.path.insert(0, backend_dir)
    
    # Import and run the backend main
    from main import app
    import uvicorn
    
    # Get port from environment (Railway requirement)
    port = int(os.environ.get("PORT", 8000))
    
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
