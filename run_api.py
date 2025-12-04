#!/usr/bin/env python3
"""Run the Thinking Engine API server."""

import os
import uvicorn
from src.thinking_engine.api import app

if __name__ == "__main__":
    # Get port from environment (Render sets PORT env var)
    port = int(os.getenv("PORT", 8000))
    # Only reload in development (when DEBUG is set)
    reload = os.getenv("DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=reload
    )

