from tools import get_users
from fastmcp import FastMCP

users = get_users(limit=10)

userid = get_users(user_id=60)
print(userid)
print(users)