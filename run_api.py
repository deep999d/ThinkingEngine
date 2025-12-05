#!/usr/bin/env python3
"""Start the Thinking Engine API server."""

import os
import uvicorn
from src.thinking_engine.api import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=reload
    )
