from openai import OpenAI
import os
from dotenv import load_dotenv
import redis

load_dotenv()

class ModelLoader:
    def __init__(self):
        """
        llm class init
        """
        self.model = OpenAI(
            api_key = os.getenv('MODEL_API_KEY'),
            base_url = os.getenv('BASE_URL'))
        
        self.model_name = os.getenv('MODEL_NAME')

    def chat(self, messages, memory=None, sys_prompt=None, tools=None, extra=None):
        """
        function for handling chat function

        messages: current messages
        memory: default to None, can be loaded from self.load_memory
        sys_prompt: default to None, can be loaded from lib/prompts/*_prompt.py, usually loaded on sub-classes of this which is agents
        tools: default to None, can be loaded from lib/utils/tools/*_tool.py, usually loaded on sub-classes of this which is agents
        extra: extra parameter for the model, example for extra param:
        {
            "model": "some-model",
            "messages": [...],
            "temperature": 0.7,
            "max_tokens": 256,
            "top_p": 0.95
        }


        """
        payload = {
            "model": self.model_name,
            "messages": messages,
        }

        if sys_prompt:
            payload["messages"].insert(0, {"role": "system", "content": sys_prompt})
        
        if tools:
            payload["tools"] = tools

        if extra:
            payload.update(extra)

        response = self.model.chat.completions.create(**payload)
        return response.choices[0].message.content
    
    def save_memory(self, messages):
        """
        function for saving chat memories in session context
        """
        pass

    def load_memory(self, messages):
        """
        function for loading chat memories in session context
        """
        pass
