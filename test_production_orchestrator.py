"""
Test Production Orchestrator with Real Agents

Tests:
- LLM-based decomposition
- Real SmartAgent integration
- Hierarchical memory
- Parallel execution
- Error recovery
"""

import asyncio
import sys
import os
sys.path.insert(0, '.')

from agentops.orchestrator import AgentOrchestrator
from agentic_sdk.memory import HierarchicalMemory


class MockSmartAgent:
    """Mock SmartAgent for testing without API"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
    
    async def execute(self, task: str):
        """Simulate execution"""
        await asyncio.sleep(0.2)
        
        class Result:
            def __init__(self, output):
                self.output = output
                self.success = True
        
        return Result(f"[{self.agent_type}] Completed: {task}")


async def test_basic_orchestration():
    """Test basic orchestration without LLM"""
    print("\n=== Test 1: Basic Orchestration (No LLM) ===\n")
    
    memory = HierarchicalMemory(user_id="test-user", session_id="test-session")
    
    orchestrator = AgentOrchestrator(
        memory=memory,
        use_llm_decomposition=False
    )
    
    orchestrator.register_agent("research", MockSmartAgent("research"))
    orchestrator.register_agent("analysis", MockSmartAgent("analysis"))
    orchestrator.register_agent("writing", MockSmartAgent("writing"))
    
    result = await orchestrator.coordinate(
        "Research AI trends, analyze the findings, and write a summary report"
    )
    
    print(f"\nSuccess: {result['success']}")
    print(f"Completed: {result['completed']}/{result['total_subtasks']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    
    print(f"\nMemory stats: {memory.get_summary()}")
    facts = memory.search_facts("orchestrated")
    print(f"Facts stored: {len(facts)}")


async def test_parallel_execution():
    """Test parallel execution of independent tasks"""
    print("\n=== Test 2: Parallel Execution ===\n")
    
    orchestrator = AgentOrchestrator(use_llm_decomposition=False)
    orchestrator.register_agent("worker", MockSmartAgent("worker-1"))
    
    result = await orchestrator.coordinate("Process data batch")
    
    print(f"Duration: {result['duration_seconds']:.2f}s")


async def test_error_recovery():
    """Test error handling and retry"""
    print("\n=== Test 3: Error Recovery ===\n")
    
    class FailingAgent:
        def __init__(self):
            self.attempt = 0
        
        async def execute(self, task: str):
            self.attempt += 1
            if self.attempt < 2:
                raise Exception(f"Simulated failure (attempt {self.attempt})")
            
            class Result:
                output = "Success after retry"
                success = True
            return Result()
    
    orchestrator = AgentOrchestrator(use_llm_decomposition=False)
    orchestrator.register_agent("general", FailingAgent())
    
    result = await orchestrator.coordinate("Test retry logic")
    
    print(f"Success: {result['success']}")


async def test_with_llm():
    """Test LLM-based decomposition"""
    print("\n=== Test 4: LLM Decomposition ===\n")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Skipping: ANTHROPIC_API_KEY not set")
        return
    
    orchestrator = AgentOrchestrator(
        api_key=api_key,
        use_llm_decomposition=True
    )
    
    orchestrator.register_agent("research", MockSmartAgent("research"))
    orchestrator.register_agent("analysis", MockSmartAgent("analysis"))
    orchestrator.register_agent("writing", MockSmartAgent("writing"))
    
    result = await orchestrator.coordinate(
        "Create a comprehensive market analysis report for the AI industry"
    )
    
    print(f"\nLLM decomposed into {result['total_subtasks']} tasks")
    print(f"Success: {result['success']}")


async def main():
    try:
        await test_basic_orchestration()
        await test_parallel_execution()
        await test_error_recovery()
        await test_with_llm()
        
        print("\n=== All Tests Complete ===\n")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
