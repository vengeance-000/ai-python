from typing import Dict, List, Callable, Any
from langchain.tools import BaseTool
from pydantic import BaseModel
import importlib
import inspect

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.tool_categories: Dict[str, List[str]] = {}
        
    def register_tool(self, tool: BaseTool, category: str = "general"):
        """Register a tool with the registry"""
        self.tools[tool.name] = tool
        if category not in self.tool_categories:
            self.tool_categories[category] = []
        self.tool_categories[category].append(tool.name)
        
    def get_tools_by_category(self, category: str) -> List[BaseTool]:
        """Get all tools in a category"""
        if category not in self.tool_categories:
            return []
        return [self.tools[name] for name in self.tool_categories[category]]
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools"""
        return list(self.tools.values())
    
    def auto_discover_tools(self, module_path: str):
        """Auto-discover tools from a module"""
        module = importlib.import_module(module_path)
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, BaseTool) and 
                obj != BaseTool):
                tool_instance = obj()
                self.register_tool(tool_instance)

# Global tool registry
tool_registry = ToolRegistry()