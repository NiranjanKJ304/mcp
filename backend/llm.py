from groq import Groq
from backend.config import settings


class GroqLLM:

    def __init__(self):
        self.client = Groq(
            api_key=settings.groq_api_key
        )

    def chat(self, messages, tools=None):

        kwargs = {
            "model": settings.model,
            "messages": messages,
            "temperature": 0
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        return self.client.chat.completions.create(**kwargs)
