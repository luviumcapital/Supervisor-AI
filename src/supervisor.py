"""Supervisor Orchestrator Module

Core supervisor that manages agent coordination, task delegation, and orchestration.
"""

import asyncio
from typing import Dict, List, Any, Optional
from .agent_management import Agent, AgentRegistry, AgentCapability
import logging

logger = logging.getLogger(__name__)


class SupervisorOrchestrator:
    """Main supervisor for orchestrating multi-agent tasks."""

    def __init__(self, name: str = "Supervisor"):
        """Initialize the supervisor.
        
        Args:
            name: Supervisor name
        """
        self.name = name
        self.registry = AgentRegistry()
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.running = False

    def register_agent(self, agent: Agent) -> None:
        """Register an agent with the supervisor.
        
        Args:
            agent: Agent to register
        """
        self.registry.register(agent)
        logger.info(f"Agent {agent.name} registered with supervisor")

    async def initialize_agents(self) -> None:
        """Initialize all registered agents."""
        agents = self.registry.list_all_agents()
        for agent in agents:
            await agent.initialize()
        logger.info(f"Initialized {len(agents)} agents")

    async def shutdown_agents(self) -> None:
        """Shutdown all registered agents."""
        agents = self.registry.list_all_agents()
        for agent in agents:
            await agent.shutdown()
        logger.info(f"Shutdown {len(agents)} agents")

    async def delegate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a task to appropriate agent(s).
        
        Args:
            task: Task dictionary with 'capability' and 'data' keys
            
        Returns:
            Result dictionary from agent execution
        """
        required_capability = task.get('capability')
        if not required_capability:
            raise ValueError("Task must specify a capability")
        
        # Find agents with required capability
        agents = self.registry.get_agents_by_capability(
            AgentCapability(required_capability)
        )
        
        if not agents:
            return {
                "success": False,
                "error": f"No agents available for capability: {required_capability}"
            }
        
        # Use first available agent
        agent = agents[0]
        logger.info(f"Delegating task to agent {agent.name}")
        
        try:
            result = await agent.execute(task)
            return {
                "success": True,
                "agent_id": agent.agent_id,
                "agent_name": agent.name,
                "result": result
            }
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": agent.agent_id
            }

    async def start(self) -> None:
        """Start the supervisor."""
        self.running = True
        await self.initialize_agents()
        logger.info(f"{self.name} started")

    async def stop(self) -> None:
        """Stop the supervisor."""
        self.running = False
        await self.shutdown_agents()
        logger.info(f"{self.name} stopped")

    def get_status(self) -> Dict[str, Any]:
        """Get supervisor status."""
        return {
            "supervisor": self.name,
            "running": self.running,
            "registry": self.registry.get_registry_status()
        }
