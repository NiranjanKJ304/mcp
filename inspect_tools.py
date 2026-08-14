import asyncio

from mcp_client import GitHubMCPClient


async def main():

    github = GitHubMCPClient()

    await github.connect()

    try:

        tools = await github.list_tools()

        for tool in tools:

            if tool.name in [
                "get_me",
                "search_repositories",
                "get_file_contents",
            ]:

                print("\n" + "=" * 70)
                print("TOOL:", tool.name)
                print("DESCRIPTION:", tool.description)
                print("SCHEMA:")
                print(tool.inputSchema)

    finally:

        await github.disconnect()


if __name__ == "__main__":
    asyncio.run(main())