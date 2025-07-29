from typing import Dict, Any, Type
from ..agents.base_agent import BaseAgent
from ..agents.research_agent import ResearchAgent
from ..tools.tool_registry import tool_registry

class AgentFactory:
    def __init__(self, model_loader, memory_controller):
        self.model_loader = model_loader
        self.memory_controller = memory_controller
        self.agent_types: Dict[str, Type[BaseAgent]] = {
            "research": ResearchAgent,
            # Add more agent types here
        }
        self.active_agents: Dict[str, BaseAgent] = {}
        
    def get_agent(self, agent_type: str) -> BaseAgent:
        """Get or create an agent of the specified type"""
        if agent_type not in self.active_agents:
            if agent_type not in self.agent_types:
                raise ValueError(f"Unknown agent type: {agent_type}")
                
            agent_class = self.agent_types[agent_type]
            self.active_agents[agent_type] = agent_class(
                self.model_loader, 
                self.memory_controller
            )
            
        return self.active_agents[agent_type]
        
    def create_agent_from_config(self, config: Dict[str, Any]) -> BaseAgent:
        """Create a custom agent from configuration"""
        # Implementation for dynamic agent creation
        pass