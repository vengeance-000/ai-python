from .base_agent import BaseAgent
from langgraph.graph import MessagesState
from ..tools.tool_registry import tool_registry

class ResearchAgent(BaseAgent):
    def __init__(self, model_loader, memory_controller):
        research_tools = tool_registry.get_tools_by_category("research")
        super().__init__("research", model_loader, memory_controller, research_tools)
    
    def _get_state_schema(self):
        class ResearchState(MessagesState):
            research_query: str = ""
            sources: list[str] = []
            findings: list[str] = []
        return ResearchState
    
    def _agent_node(self, state):
        messages = state["messages"]
        system_prompt = """You are a research agent. Your job is to:
        1. Understand the research query
        2. Use available tools to gather information
        3. Synthesize findings into a comprehensive response
        
        Available tools: web search, document retrieval, fact checking
        """
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        response = self.model_loader.model.bind_tools(self.tools).invoke(full_messages)
        return {"messages": [response]}