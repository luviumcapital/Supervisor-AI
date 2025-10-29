"""Agent Registry Module

Manages registration, discovery, and lifecycle of agents in the system.
"""

from typing import Dict, List, Optional, Type
from .agent_base import Agent, AgentCapability
import logging

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry for managing agents in the system."""

    def __init__(self):
        """Initialize the registry."""
        self._agents: Dict[str, Agent] = {}
        self._agents_by_capability: Dict[AgentCapability, List[str]] = {}
        for cap in AgentCapability:
            self._agents_by_capability[cap] = []

    def register(self, agent: Agent) -> None:
        """Register an agent.
        
        Args:
            agent: Agent instance to register
        """
        agent_id = agent.agent_id
        if agent_id in self._agents:
            logger.warning(f"Agent {agent_id} already registered, overwriting")
        
        self._agents[agent_id] = agent
        
        for capability in agent.capabilities:
            if agent_id not in self._agents_by_capability[capability]:
                self._agents_by_capability[capability].append(agent_id)
        
        logger.info(f"Registered agent {agent.name} ({agent_id})")

    def unregister(self, agent_id: str) -> bool:
        """Unregister an agent.
        
        Args:
            agent_id: ID of agent to unregister
            
        Returns:
            True if agent was unregistered, False if not found
        """
        if agent_id not in self._agents:
            return False
        
        agent = self._agents.pop(agent_id)
        
        for capability in agent.capabilities:
            if agent_id in self._agents_by_capability[capability]:
                self._agents_by_capability[capability].remove(agent_id)
        
        logger.info(f"Unregistered agent {agent.name} ({agent_id})")
        return True

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID.
        
        Args:
            agent_id: ID of agent
            
        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(agent_id)

    def get_agents_by_capability(self, capability: AgentCapability) -> List[Agent]:
        """Get agents with a specific capability.
        
        Args:
            capability: Capability to search for
            
        Returns:
            List of agents with the capability
        """
        agent_ids = self._agents_by_capability.get(capability, [])
        return [self._agents[aid] for aid in agent_ids if aid in self._agents]

    def list_all_agents(self) -> List[Agent]:
        """List all registered agents.
        
        Returns:
            List of all agents
        """
        return list(self._agents.values())

    def get_registry_status(self) -> Dict:
        """Get registry status.
        
        Returns:
            Dictionary with registry statistics
        """
        return {
            "total_agents": len(self._agents),
            "agents_by_capability": {
                cap.value: len(agent_ids)
                for cap, agent_ids in self._agents_by_capability.items()
            },
            "agent_details": [
                agent.get_status() for agent in self._agents.values()
            ]
        }
