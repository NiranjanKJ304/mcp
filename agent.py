import json

from llm import GroqLLM
from mcp_client import GitHubMCPClient


class GitHubAgent:

    def __init__(self):

        self.llm = GroqLLM()
        self.mcp = GitHubMCPClient()

    async def ask(self, question: str):

        await self.mcp.connect()

        try:

            # --------------------------------
            # 1. Discover MCP tools
            # --------------------------------

            mcp_tools = await self.mcp.list_tools()

            tools = []

            for tool in mcp_tools:

                tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": tool.inputSchema,
                        },
                    }
                )

            # --------------------------------
            # 2. User message
            # --------------------------------

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a GitHub assistant. "
                        "Use the available GitHub tools when "
                        "the user asks for GitHub information. "
                        "Do not invent GitHub data."
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ]

            # --------------------------------
            # 3. Ask Groq
            # --------------------------------

            response = self.llm.chat(
                messages=messages,
                tools=tools,
            )

            message = response.choices[0].message

            # --------------------------------
            # 4. No tool required
            # --------------------------------

            if not message.tool_calls:

                return message.content

            # --------------------------------
            # 5. Process tool calls
            # --------------------------------

            messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments,
                            },
                        }
                        for call in message.tool_calls
                    ],
                }
            )

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(
                    f"Calling MCP tool: "
                    f"{tool_name}"
                )

                print(
                    f"Arguments: {arguments}"
                )

                # --------------------------------
                # 6. Call GitHub MCP
                # --------------------------------

                result = await self.mcp.call_tool(
                    tool_name,
                    arguments,
                )

                # --------------------------------
                # 7. Send result back to Groq
                # --------------------------------

                if result.is_error:

                    tool_result = {
                        "error": str(result)
                    }

                else:

                    if result.data is not None:
                        tool_result = result.data

                    else:
                        tool_result = str(result)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            tool_result,
                            default=str
                        ),
                    }
                )

            # --------------------------------
            # 8. Final Groq response
            # --------------------------------

            final_response = self.llm.chat(
                messages=messages
            )

            return (
                final_response
                .choices[0]
                .message
                .content
            )

        finally:

            await self.mcp.disconnect()

