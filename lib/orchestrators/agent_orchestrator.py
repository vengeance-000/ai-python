from typing import Dict, List, Any
from ..agents.base_agent import BaseAgent
import asyncio
import datetime


class AgentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, List[str]] = {}
        
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        
    def create_workflow(self, name: str, agent_sequence: List[str]):
        """Create a multi-agent workflow"""
        self.workflows[name] = agent_sequence
        
    async def execute_workflow(self, workflow_name: str, initial_input: Dict, thread_id: str):
        """Execute a multi-agent workflow"""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow {workflow_name} not found")
            
        agent_sequence = self.workflows[workflow_name]
        current_state = initial_input
        results = []
        
        for agent_name in agent_sequence:
            if agent_name not in self.agents:
                raise ValueError(f"Agent {agent_name} not found")
                
            agent = self.agents[agent_name]
            result = await agent.invoke(current_state, f"{thread_id}_{agent_name}")
            results.append({
                "agent": agent_name,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            # Update state for next agent
            current_state = self._merge_states(current_state, result)
            
        return {
            "workflow": workflow_name,
            "results": results,
            "final_state": current_state
        }
        
    def _merge_states(self, current: Dict, new: Dict) -> Dict:
        """Merge states between agents"""
        merged = current.copy()
        merged.update(new)
        return merged