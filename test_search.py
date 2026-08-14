import asyncio

from mcp_client import GitHubMCPClient


async def main():

    github = GitHubMCPClient()

    await github.connect()

    try:

        print("Searching repositories...\n")

        result = await github.call_tool(
            "search_repositories",
            {
                "query": "user:NiranjanKJ304 is:public",
                "perPage": 100,
                "minimal_output": True,
            },
        )

        print(result)

    finally:

        await github.disconnect()


if __name__ == "__main__":
    asyncio.run(main())