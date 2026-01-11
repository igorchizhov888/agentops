"""
AgentOps - Enterprise Platform for AI Agent Operations

Built on top of agentic_sdk with:
- Framework integrations (LangChain, CrewAI, AutoGen)
- REST API and Web Dashboard
- PostgreSQL storage for multi-instance deployments
- Enterprise authentication and RBAC
"""

__version__ = "1.0.0"

# Import core components from agentic_sdk
from agentic_sdk.observability import AgentTracer
from agentic_sdk.prompts import PromptManager
from agentic_sdk.eval import AgentEvaluator
from agentic_sdk.registry import ToolRegistry
from agentic_sdk.ab_testing import ABTester

__all__ = [
    'AgentTracer',
    'PromptManager',
    'AgentEvaluator',
    'ToolRegistry',
    'ABTester',
]
