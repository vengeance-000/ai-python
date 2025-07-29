from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
import logging

class BaseAgent(ABC):
    def __init__(self, name: str, model_loader, memory_controller, tools: List = None):
        self.name = name
        self.model_loader = model_loader
        self.memory_controller = memory_controller
        self.tools = tools or []
        self.logger = logging.getLogger(f"{__name__}.{name}")
        self.graph = self._build_graph()
        
    def _build_graph(self):
        """Build the agent's workflow graph"""
        workflow = StateGraph(state_schema=self._get_state_schema())
        
        # Add nodes
        workflow.add_node("agent", self._agent_node)
        if self.tools:
            workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_node("response", self._response_node)
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": "response"
            }
        )
        workflow.add_edge("tools", "agent")
        workflow.add_edge("response", END)
        
        return workflow.compile(checkpointer=self.memory_controller.memory)
    
    @abstractmethod
    def _get_state_schema(self):
        """Define the state schema for this agent"""
        pass
    
    @abstractmethod
    def _agent_node(self, state):
        """Main agent logic"""
        pass
    
    def _should_continue(self, state):
        """Decide whether to use tools or end"""
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        return "end"
    
    def _response_node(self, state):
        """Final response processing"""
        return state
    
    async def invoke(self, input_data: Dict, thread_id: str = "default"):
        """Invoke the agent with memory"""
        config = {"configurable": {"thread_id": thread_id}}
        return await self.graph.ainvoke(input_data, config=config)