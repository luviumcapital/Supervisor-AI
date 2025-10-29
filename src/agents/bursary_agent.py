"""Bursary Management Agent

Specialized agent for managing scholarship programs, funding applications, and student support.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from ..agent_management import Agent, AgentCapability

logger = logging.getLogger(__name__)


class BursaryManagementAgent(Agent):
    """Agent for bursary management and scholarship administration."""

    def __init__(self, agent_id: str = "agent_bursary_001"):
        """Initialize the Bursary Management Agent.
        
        Args:
            agent_id: Unique identifier for the agent
        """
        super().__init__(
            agent_id=agent_id,
            name="Bursary Manager",
            capabilities=[
                AgentCapability("scholarship_management"),
                AgentCapability("application_processing"),
                AgentCapability("fund_disbursement"),
                AgentCapability("student_support")
            ]
        )

    async def initialize(self) -> None:
        """Initialize the agent."""
        logger.info(f"{self.name} initialized")
        self.state = {
            "active_scholarships": 0,
            "pending_applications": [],
            "total_funds_disbursed": 0.0,
            "initialized_at": datetime.now().isoformat()
        }

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a bursary management task.
        
        Args:
            task: Task dictionary containing action and parameters
            
        Returns:
            Result of the bursary task
        """
        action = task.get("action", "")
        
        if action == "process_application":
            return await self._process_application(task.get("data", {}))
        elif action == "evaluate_eligibility":
            return await self._evaluate_eligibility(task.get("data", {}))
        elif action == "disburse_funds":
            return await self._disburse_funds(task.get("data", {}))
        elif action == "provide_support":
            return await self._provide_support(task.get("data", {}))
        else:
            return {"error": f"Unknown action: {action}"}

    async def _process_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process scholarship application."""
        student_id = data.get("student_id")
        scholarship_type = data.get("scholarship_type")
        
        application = {
            "application_id": f"APP_{datetime.now().timestamp()}",
            "student_id": student_id,
            "scholarship_type": scholarship_type,
            "status": "received",
            "application_timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Application processed for student {student_id}")
        return application

    async def _evaluate_eligibility(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate student eligibility."""
        student_id = data.get("student_id")
        gpa = data.get("gpa", 0)
        income_level = data.get("income_level")
        
        eligibility = {
            "student_id": student_id,
            "eligible": gpa >= 3.0 and income_level == "low",
            "gpa_criteria_met": gpa >= 3.0,
            "financial_criteria_met": income_level == "low",
            "eligibility_score": 0.85 if gpa >= 3.5 else 0.70,
            "evaluation_timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Eligibility evaluation completed for student {student_id}")
        return eligibility

    async def _disburse_funds(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Disburse scholarship funds."""
        student_id = data.get("student_id")
        amount = data.get("amount", 0)
        
        disbursement = {
            "student_id": student_id,
            "amount": amount,
            "status": "disbursed",
            "transaction_id": f"TXN_{datetime.now().timestamp()}",
            "disbursement_date": datetime.now().isoformat()
        }
        
        logger.info(f"Funds disbursed to student {student_id}: ${amount}")
        return disbursement

    async def _provide_support(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide support services to students."""
        student_id = data.get("student_id")
        support_type = data.get("support_type")
        
        support_response = {
            "student_id": student_id,
            "support_type": support_type,
            "services": [
                "academic_mentoring",
                "career_counseling",
                "financial_guidance"
            ],
            "support_provided": True,
            "support_timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Support provided to student {student_id}")
        return support_response

    async def shutdown(self) -> None:
        """Shutdown the agent."""
        logger.info(f"{self.name} shutting down")
