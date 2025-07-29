from openai import OpenAI
import os


client = OpenAI(
    api_key=os.getenv('SEA_LION_API_KEY'),
    base_url="https://api.sea-lion.ai/v1" 
)

completion = client.chat.completions.create(
    model="aisingapore/Llama-SEA-LION-v3.5-8B-R",
    messages=[
        {
            "role": "user",
            "content": "Tell me a Singlish joke!"
        }
    ],
    extra_body={
        "chat_template_kwargs": {
            "thinking_mode": "off"
        }, 
        "cache": {
            "no-cache": True
        }
    },
)

print(completion.choices[0].message.content)
