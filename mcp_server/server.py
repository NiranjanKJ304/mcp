from fastmcp import FastMCP
from tools import (
    get_users,
    get_user,
    search_users
)

mcp = FastMCP("PostgreSQL MCP Server")


@mcp.tool()
def list_users(limit: int = 5):
    """
    Return the first N users.
    """
    return get_users(limit)

@mcp.tool()
def get_user_by_id(user_id: int):
    """
    Get a user by ID.
    """
    return get_user(user_id)


@mcp.tool()
def search_user(name: str):
    """
    Search users by first or last name.
    """
    return search_users(name)


if __name__ == "__main__":
    mcp.run()
from fastmcp import FastMCP
from tools import (
    get_users,
    get_user,
    search_users
)

mcp = FastMCP("PostgreSQL MCP Server")

@mcp.tool()
def list_users(limit: int = 5):
    """
    Return the first N users.
    """
    return get_users(limit)

@mcp.tool()
def get_user_by_id(user_id: int):
    """
    Get a user by ID.
    """
    return get_user(user_id)

@mcp.tool()
def search_user(name: str):
    """
    Search users by first or last name.
    """
    return search_users(name)

if __name__ == "__main__":
    mcp.run()
