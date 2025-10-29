"""Base Agent Class Module

Defines the abstract base class and interfaces for agents in the Supervisor AI system.
Provides standardized agent lifecycle management and capability tracking.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class AgentCapability(str, Enum):
    """Enumeration of agent capabilities."""
    INVOICE_PROCESSING = "invoice_processing"
    DATA_EXTRACTION = "data_extraction"
    EMAIL_SENDING = "email_sending"
    DOCUMENT_GENERATION = "document_generation"
    ERROR_HANDLING = "error_handling"
    FALLBACK_PROCESSING = "fallback_processing"
    COORDINATION = "coordination"
    REPORTING = "reporting"


class AgentState(str, Enum):
    """Enumeration of agent states."""
    IDLE = "idle"
    ACTIVE = "active"
    PROCESSING = "processing"
    ERROR = "error"
    RECOVERING = "recovering"
    SHUTDOWN = "shutdown"


class AgentMetadata(BaseModel):
    """Metadata for agents."""
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    version: str = "0.1.0"
    capabilities: List[AgentCapability]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Agent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, name: str, description: str, capabilities: List[AgentCapability]):
        """Initialize an agent.
        
        Args:
            name: Agent name
            description: Agent description
            capabilities: List of agent capabilities
        """
        self.metadata = AgentMetadata(
            name=name,
            description=description,
            capabilities=capabilities
        )
        self.state = AgentState.IDLE
        self.error_log: List[Dict[str, Any]] = []

    @property
    def agent_id(self) -> str:
        """Get agent ID."""
        return self.metadata.agent_id

    @property
    def name(self) -> str:
        """Get agent name."""
        return self.metadata.name

    @property
    def capabilities(self) -> List[AgentCapability]:
        """Get agent capabilities."""
        return self.metadata.capabilities

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task.
        
        Args:
            task: Task dictionary containing task parameters
            
        Returns:
            Result dictionary
        """
        pass

    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass

    async def initialize(self) -> None:
        """Initialize the agent."""
        self.state = AgentState.ACTIVE

    async def shutdown(self) -> None:
        """Shutdown the agent."""
        self.state = AgentState.SHUTDOWN

    def log_error(self, error: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log an error.
        
        Args:
            error: Error message
            context: Additional context
        """
        self.error_log.append({
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "context": context or {}
        })

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "state": self.state.value,
            "capabilities": [cap.value for cap in self.capabilities],
            "error_count": len(self.error_log),
            "created_at": self.metadata.created_at.isoformat(),
        }
