from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

class ModelLoader:
    def __init__(self, memory_controller):
        load_dotenv()

        self.model = ChatOpenAI(
            api_key=os.getenv("MODEL_API_KEY"),
            base_url=os.getenv("BASE_URL"),
            model=os.getenv("MODEL_NAME"),
        )
        self.model_name = os.getenv('MODEL_NAME')
        self.memory_controller = memory_controller
        
        if self.memory_controller:
            self.compiled_graph = self.memory_controller.compile_workflow(self._call_model)
        

    def _call_model(self, state):
        """Internal method used by LangGraph workflow"""
        messages = state["messages"]
        
        if hasattr(state, 'tools') and state.get('tools'):
            bound_model = self.model.bind_tools(state['tools'])
        else:
            bound_model = self.model
            
        if hasattr(state, 'extra') and state.get('extra'):
            bound_model = bound_model.bind(**state['extra'])
            
        response = bound_model.invoke(messages)
        return {"messages": [response]}

    def chat(self, tid, messages, sys_prompt=None, tools=None, extra=None):
        if sys_prompt:
            messages = [{"role": "system", "content": sys_prompt}] + messages
        
        if self.memory_controller:
            input_data = {
                "messages": messages,
                "tools": tools,
                "extra": extra
            }
            result = self.memory_controller.invoke_with_memory(
                self.compiled_graph, 
                input_data, 
                tid
            )
            return result["messages"][-1].content
        else:
            model = self.model
            if tools:
                model = model.bind_tools(tools)
            if extra:
                model = model.bind(**extra)
            
            response = model.invoke(messages)
            return response.content
