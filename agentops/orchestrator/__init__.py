"""
Agent Orchestrator Module

Multi-agent coordination for complex tasks:
- LLM-based task decomposition
- Agent assignment and coordination
- Dependency management
- Parallel execution
- Error recovery
- Result aggregation
"""

from .agent_orchestrator import AgentOrchestrator, AgentTask
from .llm_decomposer import LLMTaskDecomposer

__all__ = ['AgentOrchestrator', 'AgentTask', 'LLMTaskDecomposer']
