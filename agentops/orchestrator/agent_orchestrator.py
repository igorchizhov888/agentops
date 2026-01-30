"""
Multi-Agent Orchestrator - Production Version

Coordinates multiple agents working together on complex tasks.
Features:
- LLM-based task decomposition
- Real agent integration with SmartAgent
- Hierarchical memory integration
- Parallel execution of independent tasks
- Complex dependency graphs
- Error handling and recovery
"""

from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime
import asyncio
from agentic_sdk.memory import HierarchicalMemory
from .llm_decomposer import LLMTaskDecomposer


class AgentTask:
    """Represents a subtask for an agent"""
    
    def __init__(self, task_id: str, description: str, agent_type: str, 
                 dependencies: List[str] = None, estimated_duration: int = 3):
        self.task_id = task_id
        self.description = description
        self.agent_type = agent_type
        self.dependencies = dependencies or []
        self.estimated_duration = estimated_duration
        self.status = "pending"
        self.result = None
        self.error = None
        self.assigned_agent = None
        self.started_at = None
        self.completed_at = None
        self.retry_count = 0
        self.max_retries = 2
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "agent_type": self.agent_type,
            "dependencies": self.dependencies,
            "estimated_duration": self.estimated_duration,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "assigned_agent": self.assigned_agent,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "retry_count": self.retry_count
        }


class AgentOrchestrator:
    """
    Coordinates multiple agents to accomplish complex tasks.
    
    Production features:
    - LLM-based intelligent task decomposition
    - Real SmartAgent integration
    - Hierarchical memory for shared context
    - Parallel execution of independent tasks
    - Error recovery with retries
    - Complex dependency management
    """
    
    def __init__(self, memory: Optional[HierarchicalMemory] = None, 
                 api_key: str = None, use_llm_decomposition: bool = True):
        """
        Initialize orchestrator.
        
        Args:
            memory: HierarchicalMemory instance for shared context
            api_key: Anthropic API key for LLM decomposition
            use_llm_decomposition: Use LLM for smart decomposition
        """
        self.orchestrator_id = str(uuid4())
        self.agents = {}
        self.memory = memory
        self.execution_history = []
        
        # LLM decomposer
        self.use_llm = use_llm_decomposition
        self.decomposer = None
        if use_llm_decomposition and api_key:
            try:
                self.decomposer = LLMTaskDecomposer(api_key=api_key)
            except Exception as e:
                print(f"LLM decomposer init failed: {e}, using fallback")
                self.use_llm = False
    
    def register_agent(self, agent_type: str, agent_instance: Any) -> None:
        """Register an agent with the orchestrator"""
        self.agents[agent_type] = agent_instance
        
        if self.memory:
            self.memory.store(
                f"agent_{agent_type}_registered",
                {"type": agent_type, "timestamp": datetime.now().isoformat()},
                level="long_term",
                category="orchestrator"
            )
        
        print(f"Registered agent: {agent_type}")
    
    def decompose_task(self, task: str) -> List[AgentTask]:
        """
        Decompose complex task into subtasks.
        Uses LLM if available, otherwise falls back to keyword matching.
        """
        available_agents = list(self.agents.keys())
        
        # Try LLM decomposition first
        if self.use_llm and self.decomposer:
            try:
                subtask_dicts = self.decomposer.decompose(task, available_agents)
                subtasks = [
                    AgentTask(
                        task_id=st["task_id"],
                        description=st["description"],
                        agent_type=st["agent_type"],
                        dependencies=st.get("dependencies", []),
                        estimated_duration=st.get("estimated_duration", 3)
                    )
                    for st in subtask_dicts
                ]
                return subtasks
            except Exception as e:
                print(f"LLM decomposition failed: {e}, using fallback")
        
        # Fallback: simple keyword matching
        return self._fallback_decompose(task, available_agents)
    
    def _fallback_decompose(self, task: str, agents: List[str]) -> List[AgentTask]:
        """Simple keyword-based decomposition"""
        subtasks = []
        task_lower = task.lower()
        
        if "research" in task_lower or "find" in task_lower:
            subtasks.append(AgentTask(
                task_id="task-1",
                description=f"Research: {task}",
                agent_type="research" if "research" in agents else agents[0]
            ))
        
        if "analyze" in task_lower:
            subtasks.append(AgentTask(
                task_id=f"task-{len(subtasks)+1}",
                description="Analyze findings",
                agent_type="analysis" if "analysis" in agents else agents[0],
                dependencies=[subtasks[-1].task_id] if subtasks else []
            ))
        
        if "write" in task_lower or "report" in task_lower:
            subtasks.append(AgentTask(
                task_id=f"task-{len(subtasks)+1}",
                description="Write report",
                agent_type="writing" if "writing" in agents else agents[0],
                dependencies=[subtasks[-1].task_id] if subtasks else []
            ))
        
        if not subtasks:
            subtasks.append(AgentTask(
                task_id="task-1",
                description=task,
                agent_type=agents[0] if agents else "general"
            ))
        
        return subtasks
    
    async def execute_task(self, task: AgentTask) -> AgentTask:
        """Execute a single subtask with error recovery"""
        agent = self.agents.get(task.agent_type)
        
        if not agent:
            task.status = "failed"
            task.error = f"No agent registered for type: {task.agent_type}"
            return task
        
        task.status = "running"
        task.started_at = datetime.now().isoformat()
        task.assigned_agent = task.agent_type
        
        while task.retry_count <= task.max_retries:
            try:
                # Execute with agent
                result = await agent.execute(task.description)
                
                task.status = "completed"
                task.result = result.output if hasattr(result, 'output') else str(result)
                task.completed_at = datetime.now().isoformat()
                
                # Store result in shared memory
                if self.memory:
                    self.memory.store(
                        f"task_{task.task_id}_result",
                        task.result,
                        level="working"
                    )
                
                return task
                
            except Exception as e:
                task.retry_count += 1
                if task.retry_count > task.max_retries:
                    task.status = "failed"
                    task.error = f"Failed after {task.max_retries} retries: {str(e)}"
                    task.completed_at = datetime.now().isoformat()
                else:
                    print(f"Task {task.task_id} retry {task.retry_count}/{task.max_retries}")
                    await asyncio.sleep(1)
        
        return task
    
    def get_ready_tasks(self, tasks: List[AgentTask]) -> List[AgentTask]:
        """Get tasks ready to execute (dependencies met)"""
        ready = []
        
        for task in tasks:
            if task.status != "pending":
                continue
            
            deps_met = True
            for dep_id in task.dependencies:
                dep_task = next((t for t in tasks if t.task_id == dep_id), None)
                if not dep_task or dep_task.status != "completed":
                    deps_met = False
                    break
            
            if deps_met:
                ready.append(task)
        
        return ready
    
    async def coordinate(self, complex_task: str) -> Dict[str, Any]:
        """Coordinate multiple agents to accomplish complex task"""
        start_time = datetime.now()
        
        print(f"\nOrchestrating: {complex_task}\n")
        
        # Decompose into subtasks
        subtasks = self.decompose_task(complex_task)
        print(f"Decomposed into {len(subtasks)} subtasks:")
        for task in subtasks:
            deps = f"[depends on: {', '.join(task.dependencies)}]" if task.dependencies else ""
            print(f"  {task.task_id}: {task.description} [{task.agent_type}] {deps}")
        
        # Store in memory
        if self.memory:
            self.memory.store("orchestration_task", complex_task, level="working")
            self.memory.store("subtasks", [t.to_dict() for t in subtasks], level="working")
        
        # Execute tasks respecting dependencies
        iteration = 0
        max_iterations = 50
        
        while any(t.status == "pending" for t in subtasks) and iteration < max_iterations:
            iteration += 1
            ready_tasks = self.get_ready_tasks(subtasks)
            
            if not ready_tasks:
                pending = [t for t in subtasks if t.status == "pending"]
                if pending:
                    print(f"\nWarning: {len(pending)} tasks stuck")
                    for t in pending:
                        print(f"  {t.task_id} waiting for: {t.dependencies}")
                break
            
            # Execute ready tasks in parallel
            print(f"\nIteration {iteration}: Executing {len(ready_tasks)} tasks in parallel")
            await asyncio.gather(*[self.execute_task(task) for task in ready_tasks])
        
        # Aggregate results
        completed = [t for t in subtasks if t.status == "completed"]
        failed = [t for t in subtasks if t.status == "failed"]
        
        final_output = "\n\n".join([
            f"{t.task_id} ({t.agent_type}):\n{t.result}"
            for t in completed
        ])
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        success = len(completed) == len(subtasks)
        
        result = {
            "orchestrator_id": self.orchestrator_id,
            "task": complex_task,
            "subtasks": [t.to_dict() for t in subtasks],
            "total_subtasks": len(subtasks),
            "completed": len(completed),
            "failed": len(failed),
            "success": success,
            "final_output": final_output,
            "duration_seconds": duration,
            "started_at": start_time.isoformat(),
            "completed_at": end_time.isoformat()
        }
        
        # Store in history
        self.execution_history.append(result)
        
        # Store in long-term memory
        if self.memory and success:
            self.memory.store_fact(
                f"Successfully orchestrated: {complex_task}",
                confidence=0.95,
                source="orchestrator"
            )
        
        return result
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get orchestration execution history"""
        return self.execution_history
