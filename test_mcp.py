import asyncio

# pyrefly: ignore [missing-import]
from mcp_client import GitHubMCPClient

async def main():

    github = GitHubMCPClient()

    print("Connecting to GitHub MCP...")

    tools = await github.list_tools()

    print("\nAvailable GitHub MCP tools:\n")

    for tool in tools:

        print("=" * 70)

        print("Name:")
        print(tool.name)

        print("\nDescription:")
        print(tool.description)

        print("\nInput Schema:")
        print(tool.inputSchema)


if __name__ == "__main__":
    asyncio.run(main())