from groq import Groq

from config import GROQ_API_KEY, MODEL


class GroqLLM:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = MODEL

    def chat(
        self,
        messages,
        tools=None
    ):

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        return self.client.chat.completions.create(
            **kwargs
        )