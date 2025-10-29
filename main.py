#!/usr/bin/env python
"""
Main Application Entry Point for Supervisor AI

Starts the FastAPI/Uvicorn server with the supervisor orchestrator.
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    print("FastAPI not installed. Install with: pip install fastapi uvicorn")
    exit(1)

from src.supervisor import SupervisorOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize supervisor globally
supervisor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    global supervisor
    # Startup
    logger.info("Starting Supervisor AI...")
    supervisor = SupervisorOrchestrator(name="Luvium-Supervisor")
    await supervisor.start()
    yield
    # Shutdown
    logger.info("Shutting down Supervisor AI...")
    await supervisor.stop()

app = FastAPI(
    title="Supervisor AI",
    description="Multi-agent supervisor system for orchestrating specialized AI agents",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "online", "service": "Supervisor AI", "version": "0.1.0"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    global supervisor
    if supervisor and supervisor.running:
        return {"status": "healthy", "running": True}
    return {"status": "degraded", "running": False}

@app.get("/status")
async def status():
    """Get supervisor status."""
    global supervisor
    if supervisor:
        return supervisor.get_status()
    return {"error": "Supervisor not initialized"}

@app.post("/task/delegate")
async def delegate_task(task: dict):
    """Delegate a task to appropriate agent(s)."""
    global supervisor
    if not supervisor:
        return JSONResponse({"error": "Supervisor not initialized"}, status_code=503)
    
    try:
        result = await supervisor.delegate_task(task)
        return result
    except Exception as e:
        logger.error(f"Task delegation failed: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=400)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("ENV", "production") == "development"
    )
