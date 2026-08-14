"""Async MCP client helpers for the local server."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastmcp import Client

from .config import PROJECT_ROOT


@dataclass
class MCPServerClient:
    server_path: Path = PROJECT_ROOT / "mcp_server" / "server.py"

    async def list_tools(self) -> Any:
        async with Client(str(self.server_path)) as client:
            return await client.list_tools()

    async def call_tool(self, name: str, args: dict) -> Any:
        async with Client(str(self.server_path)) as client:
            return await client.call_tool(name, args)

def run(coro: Any) -> Any:
    return asyncio.run(coro)
