"""
LLM-based Task Decomposition

Uses Claude Haiku 4.5 to intelligently decompose complex tasks into subtasks
with proper dependencies and agent type assignment.
"""

import os
import json
from typing import List, Dict, Any
import anthropic


class LLMTaskDecomposer:
    """
    Uses LLM to decompose complex tasks into subtasks.
    
    Features:
    - Intelligent task breakdown
    - Automatic dependency detection
    - Agent type assignment
    - Complexity estimation
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def decompose(self, complex_task: str, available_agents: List[str]) -> List[Dict[str, Any]]:
        """
        Decompose complex task using LLM.
        
        Args:
            complex_task: The complex task to decompose
            available_agents: List of available agent types
            
        Returns:
            List of subtask dictionaries with dependencies
        """
        
        prompt = f"""You are a task decomposition expert. Break down this complex task into subtasks.

Complex Task: {complex_task}

Available Agent Types: {', '.join(available_agents)}

Requirements:
1. Break into 2-5 clear, actionable subtasks
2. Assign each subtask to appropriate agent type
3. Identify dependencies (which tasks must complete before others)
4. Keep subtasks atomic and focused

Return ONLY a JSON array with this structure:
[
  {{
    "task_id": "task-1",
    "description": "Clear description",
    "agent_type": "one of available types",
    "dependencies": [],
    "estimated_duration": "1-5 scale"
  }}
]

JSON array:"""

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract JSON from response
            content = response.content[0].text.strip()
            
            # Remove markdown if present
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            
            subtasks = json.loads(content)
            return subtasks
            
        except Exception as e:
            print(f"LLM decomposition failed: {e}")
            # Fallback to simple decomposition
            return self._fallback_decompose(complex_task, available_agents)
    
    def _fallback_decompose(self, task: str, agents: List[str]) -> List[Dict[str, Any]]:
        """Simple fallback if LLM fails"""
        return [{
            "task_id": "task-1",
            "description": task,
            "agent_type": agents[0] if agents else "general",
            "dependencies": [],
            "estimated_duration": 3
        }]
