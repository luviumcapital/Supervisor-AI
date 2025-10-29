"""Agents Module

Contains all specialized AI agents for the Supervisor orchestration system.
"""

from .investment_agent import InvestmentManagementAgent
from .dealer_agent import DealerOnboardingAgent
from .bursary_agent import BursaryManagementAgent
from .consulting_agent import ConsultingProposalAgent
from .government_agent import GovernmentContractingAgent
from .operations_agent import OperationsAgent
from .rd_agent import ResearchDevelopmentAgent
from .pricing_agent import PricingSpecialistAgent
from .cfo_agent import CFOAgent
from .marketing_agent import MarketingSpecialistAgent

__all__ = [
    'InvestmentManagementAgent',
    'DealerOnboardingAgent',
    'BursaryManagementAgent',
    'ConsultingProposalAgent',
    'GovernmentContractingAgent',
    'OperationsAgent',
    'ResearchDevelopmentAgent',
    'PricingSpecialistAgent',
    'CFOAgent',
    'MarketingSpecialistAgent',
]
