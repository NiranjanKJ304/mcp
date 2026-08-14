from pathlib import Path

from fastmcp import Client

from config import (
    GITHUB_PERSONAL_ACCESS_TOKEN,
    PROJECT_ROOT,
)


class GitHubMCPClient:

    def __init__(self):

        server_path = (
            PROJECT_ROOT.parent
            / "github-mcp-server"
            / "github-mcp-server.exe"
        )

        self.client = Client(
            {
                "github": {
                    "command": str(server_path),
                    "args": ["stdio","--read-only"],
                    "env": {
                        "GITHUB_PERSONAL_ACCESS_TOKEN":
                            GITHUB_PERSONAL_ACCESS_TOKEN
                    },
                }
            }
        )

    async def connect(self):
        await self.client.__aenter__()

    async def disconnect(self):
        await self.client.__aexit__(None, None, None)

    async def list_tools(self):

        async with self.client:

            return await self.client.list_tools()

    async def call_tool(
        self,
        name: str,
        arguments: dict
    ):

        async with self.client:

            return await self.client.call_tool(
                name,
                arguments
            )
