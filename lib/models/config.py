import os

class ModelConfig:
    # Enable/disable reasoning for reasoning models
    enable_reasoning: bool = True
    
    # Reasoning configuration (only used if enable_reasoning is True)
    reasoning = {
        "effort": "medium",  # 'low', 'medium', or 'high'
        "summary": "auto",  # 'detailed', 'auto', or None
    }

    extra = {
        "api_key": os.getenv("MODEL_API_KEY"),
        "base_url": os.getenv("BASE_URL"),
        "model": os.getenv("MODEL_NAME"),
    }