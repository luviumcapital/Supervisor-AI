"""
Agent Management Module

Provides core agent management functionality for the Supervisor AI system.
Includes agent registry, base classes, and orchestration utilities.
"""

from .agent_base import Agent, AgentCapability, AgentState
from .agent_registry import AgentRegistry
from .agent_pool import AgentPool

__version__ = "0.1.0"
__all__ = [
    "Agent",
    "AgentCapability",
    "AgentState",
    "AgentRegistry",
    "AgentPool",
]
