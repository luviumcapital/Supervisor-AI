#!/usr/bin/env python
"""
Main Application Entry Point for Supervisor AI

Starts the FastAPI/Uvicorn server with the supervisor orchestrator.
All agents are accessible through a single domain: app.luvium.online
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
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
    version="0.2.0",
    lifespan=lifespan
)

# Configure CORS for single domain access: app.luvium.online
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.luvium.online", "http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "online",
        "service": "Supervisor AI",
        "version": "0.2.0",
        "domain": "app.luvium.online"
    }

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

@app.get("/agents/list")
async def list_agents():
    """List all available agents."""
    global supervisor
    if supervisor:
        agents = supervisor.registry.list_all_agents()
        return {
            "total_agents": len(agents),
            "agents": [
                {
                    "id": agent.agent_id,
                    "name": agent.name,
                    "capabilities": [cap.value for cap in agent.capabilities]
                }
                for agent in agents
            ]
        }
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

@app.post("/agent/{agent_name}/task")
async def submit_agent_task(agent_name: str, task: dict):
    """Submit a task directly to a specific agent by name."""
    global supervisor
    if not supervisor:
        return JSONResponse({"error": "Supervisor not initialized"}, status_code=503)
    
    try:
        # Find agent by name
        agents = supervisor.registry.list_all_agents()
        agent = next((a for a in agents if a.name.lower() == agent_name.lower()), None)
        
        if not agent:
            return JSONResponse({"error": f"Agent '{agent_name}' not found"}, status_code=404)
        
        result = await agent.execute(task)
        return {
            "success": True,
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "result": result
        }
    except Exception as e:
        logger.error(f"Agent task execution failed: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=400)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting Supervisor AI server on {host}:{port}")
    logger.info(f"Accessible from: https://app.luvium.online")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("ENV", "production") == "development"
    )
