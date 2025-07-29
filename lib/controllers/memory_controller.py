from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
import logging

class MemoryController:
    def __init__(self):
        self.memory = InMemorySaver()
        self.logger = logging.getLogger(__name__)
        self.logger.info("MemoryController initialized")

    def compile_workflow(self, call_model_fn):
        self.logger.debug("Compiling Workflow")
        workflow = StateGraph(state_schema=MessagesState)
        workflow.add_node("model", call_model_fn)
        workflow.add_edge(START, "model")
        return workflow.compile(checkpointer=self.memory)

    def invoke_with_memory(self, compiled_graph, input_data, thread_id: str):
        """
        Proper way to use memory with LangGraph - let the compiled graph handle checkpointing
        """
        config = {"configurable": {"thread_id": thread_id}}
        return compiled_graph.invoke(input_data, config=config)
        
    def get_conversation_history(self, thread_id: str):
        """Get the conversation history for a thread"""
        config = {"configurable": {"thread_id": thread_id}}
        try:
            checkpoint = self.memory.get(config)
            if checkpoint and checkpoint.channel_values:
                return checkpoint.channel_values.get("messages", [])
            return []
        except Exception as e:
            self.logger.error(f"Error loading conversation history: {e}")
            return []