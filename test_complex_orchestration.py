"""
Test Complex Orchestration with Real SmartAgent

Tests:
1. Real SmartAgent integration from agentic_sdk
2. Complex dependency graphs (diamond pattern)
"""

import asyncio
import sys
import os
sys.path.insert(0, '.')
sys.path.insert(0, '../agentic_sdk/examples/tools')

from agentops.orchestrator import AgentOrchestrator, AgentTask
from agentic_sdk.memory import HierarchicalMemory
from agentic_sdk.runtime.smart_agent import SmartAgent
from agentic_sdk.mcp.server import MCPServer
from agentic_sdk.core.interfaces.agent import AgentConfig
from calculator_tool import CalculatorTool


async def test_real_smartagent():
    """Test with real SmartAgent from agentic_sdk"""
    print("\n=== Test 1: Real SmartAgent Integration ===\n")
    
    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        return
    
    # Setup MCP and tools
    mcp = MCPServer()
    await mcp.start()
    await mcp.register_tool(CalculatorTool())
    
    # Create real SmartAgent config
    config = AgentConfig(
        name="math_agent",
        model="claude-haiku-4-5",
        system_prompt="You are a math expert",
        max_iterations=3
    )
    
    # Create SmartAgent
    agent = SmartAgent(
        config=config,
        mcp_server=mcp,
        api_key=api_key,
        enable_memory=True,
        user_id="test-user"
    )
    
    # Create orchestrator with memory
    memory = HierarchicalMemory(user_id="test-user", session_id="test-session-1")
    orchestrator = AgentOrchestrator(
        memory=memory,
        api_key=api_key,
        use_llm_decomposition=True
    )
    
    # Register real agent
    orchestrator.register_agent("calculator", agent)
    orchestrator.register_agent("math", agent)
    orchestrator.register_agent("general", agent)
    
    # Test orchestration
    result = await orchestrator.coordinate(
        "Calculate 15 plus 25, then multiply the result by 3"
    )
    
    print(f"\nOrchestration Complete:")
    print(f"  Success: {result['success']}")
    print(f"  Subtasks: {result['completed']}/{result['total_subtasks']}")
    print(f"  Duration: {result['duration_seconds']:.2f}s")
    print(f"\nFinal Output:\n{result['final_output']}")
    
    # Check memory
    print(f"\nMemory Summary:")
    summary = memory.get_summary()
    print(f"  Working: {summary['working']['size']} items")
    print(f"  Long-term facts: {summary['long_term']['total_facts']}")
    
    await mcp.stop()


async def test_complex_dependencies():
    """Test complex dependency graph (diamond pattern)"""
    print("\n=== Test 2: Complex Dependency Graph ===\n")
    print("Pattern: A -> [B, C] -> D")
    print("  Task A must complete first")
    print("  Tasks B and C can run in parallel after A")
    print("  Task D waits for both B and C\n")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        return
    
    # Setup MCP
    mcp = MCPServer()
    await mcp.start()
    await mcp.register_tool(CalculatorTool())
    
    config = AgentConfig(
        name="calc_agent",
        model="claude-haiku-4-5",
        system_prompt="You are a calculator",
        max_iterations=3
    )
    
    agent = SmartAgent(
        config=config,
        mcp_server=mcp,
        api_key=api_key,
        enable_memory=True
    )
    
    # Create orchestrator WITHOUT LLM decomposition
    # We'll manually create complex dependencies
    orchestrator = AgentOrchestrator(
        use_llm_decomposition=False
    )
    
    orchestrator.register_agent("calculator", agent)
    
    # Manually create diamond dependency graph
    task_a = AgentTask(
        task_id="task-a",
        description="Add 10 and 5",
        agent_type="calculator",
        dependencies=[]
    )
    
    task_b = AgentTask(
        task_id="task-b",
        description="Multiply the previous result by 2",
        agent_type="calculator",
        dependencies=["task-a"]
    )
    
    task_c = AgentTask(
        task_id="task-c",
        description="Add 100 to the first result",
        agent_type="calculator",
        dependencies=["task-a"]
    )
    
    task_d = AgentTask(
        task_id="task-d",
        description="Sum all previous results",
        agent_type="calculator",
        dependencies=["task-b", "task-c"]
    )
    
    tasks = [task_a, task_b, task_c, task_d]
    
    print("Dependency Graph:")
    for t in tasks:
        deps = f" (depends on: {', '.join(t.dependencies)})" if t.dependencies else ""
        print(f"  {t.task_id}: {t.description}{deps}")
    
    # Execute manually with orchestrator's execution logic
    print("\nExecuting...")
    
    iteration = 0
    while any(t.status == "pending" for t in tasks):
        iteration += 1
        ready = orchestrator.get_ready_tasks(tasks)
        
        if not ready:
            print("No tasks ready!")
            break
        
        print(f"\nIteration {iteration}: Executing {len(ready)} tasks in parallel")
        for t in ready:
            print(f"  - {t.task_id}")
        
        await asyncio.gather(*[orchestrator.execute_task(task) for task in ready])
    
    # Results
    completed = [t for t in tasks if t.status == "completed"]
    failed = [t for t in tasks if t.status == "failed"]
    
    print(f"\nResults:")
    print(f"  Completed: {len(completed)}/{len(tasks)}")
    print(f"  Failed: {len(failed)}")
    
    print(f"\nExecution Order:")
    sorted_tasks = sorted(
        [t for t in tasks if t.completed_at],
        key=lambda x: x.completed_at
    )
    for i, t in enumerate(sorted_tasks, 1):
        print(f"  {i}. {t.task_id}: {t.result[:80]}...")
    
    await mcp.stop()


async def main():
    print("\n" + "="*70)
    print("COMPLEX ORCHESTRATION TESTS")
    print("="*70)
    
    try:
        await test_real_smartagent()
        await test_complex_dependencies()
        
        print("\n" + "="*70)
        print("ALL COMPLEX TESTS COMPLETE")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
