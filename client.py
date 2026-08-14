import asyncio

from fastmcp import Client

async def main():
    async with Client("mcp_server/server.py") as client:
        tools = await client.list_tools()
        print("Available tools:", tools)

        result = await client.call_tool(
            "get_user_by_id",
            {"user_id": 3}
        )

        print("Result:", result)

asyncio.run(main())