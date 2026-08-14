import asyncio
from mcp_client import GitHubMCPClient

async def main():
    github = GitHubMCPClient()
    try:
        print("Connecting to GitHub MCP...")
        await github.connect()
        tools = await github.list_tools()
        print("\nAvailable tools:\n")
        for tool in tools:
            print("-", tool.name)
        print("\nCalling get_me...\n")
        result = await github.call_tool("get_me", {})
        print("Result:")
        print(result)
    finally:
        await github.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
