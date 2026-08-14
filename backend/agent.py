from fastmcp.client import messages
import json

from backend.llm import GroqLLM
from backend.mcp_client import MCPServerClient


class Agent:

    def __init__(self):
        self.llm = GroqLLM()
        self.mcp = MCPServerClient()

    async def ask(self, question: str):

        # Discover available tools
        mcp_tools = await self.mcp.list_tools()

        # Convert MCP tools to Groq/OpenAI format
        tools = []

        for tool in mcp_tools:
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
            )

        messages = [
            {
                "role": "user",
                "content": question,
            }
        ]

        # Ask Groq
        response = self.llm.chat(
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message

        # -----------------------
        # No Tool Needed
        # -----------------------
        if not message.tool_calls:
            return message.content

        # -----------------------
        # Tool Call
        # -----------------------
        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print(f"\nCalling MCP Tool: {tool_name}")
        print(arguments)

        result = await self.mcp.call_tool(
            tool_name,
            arguments,
        )

        print(result)
        print(type(result))

        # Add assistant tool request
        messages.append(message)

        # Add tool result
        tool_result = result.content[0].text

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            }
        )

        # Final response
        final = self.llm.chat(messages)

        return final.choices[0].message.content
