import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

client = anthropic.Anthropic(api_key=api_key)

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=250,
    temperature=0,
    system="You are a spanish math teacher.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Explain Bayes theorem"
                }
            ]
        }
    ]
)
print(message.content)