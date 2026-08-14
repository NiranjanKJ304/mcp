# MCP Project Technical Guide

This document explains the technical architecture of this learning project, detailing how the different components communicate, with a specific focus on the request-response lifecycle driven by `test_agent.py`.

## High-Level Architecture

The project consists of three main components:
1.  **The Interface / Driver**: (e.g., `test_agent.py`) which takes user input and orchestrates the agent.
2.  **The Backend Agent (`backend/`)**: Acts as the "brain". It connects to the Groq LLM API and the local MCP (Model Context Protocol) Server.
3.  **The MCP Server (`mcp_server/`)**: Acts as the "hands". It exposes database operations as standardized tools that the Agent can call.

---

## The Request-Response Flow (Step-by-Step)

Let's walk through exactly what happens when you run `python -m tests.test_agent` and ask a question like *"Show user Mia"*.

### 1. Initialization in `test_agent.py`
```python
agent = Agent()
```
When `test_agent.py` starts, it creates an instance of `Agent` (from `backend/agent.py`). 
During its initialization, the `Agent` sets up two things:
*   `self.llm = GroqLLM()`: The connection to the Groq API (using the key from `.env`).
*   `self.mcp = MCPServerClient()`: The client that knows how to talk to our local FastMCP server.

It then enters a `while True:` loop, waiting for your input: `question = input("\nYou : ")`.

### 2. Asking the Agent
```python
answer = await agent.ask(question)
```
When you type *"Show user Mia"*, the string is passed into the `ask()` method in `backend/agent.py`. Here's what the agent does internally:

**A. Tool Discovery**
The agent asks the MCP server, *"What tools do you have?"* using `await self.mcp.list_tools()`. 
It receives a list of tools (e.g., `list_users`, `get_user_by_id`, `search_user`) and translates their schemas into a format that the Groq LLM understands (the OpenAI tool calling format).

**B. First LLM Request (Decision Making)**
The agent sends your question ("Show user Mia") along with the list of available tools to the Groq LLM.
Groq's LLM acts as a reasoning engine. It realizes: *"I don't know who Mia is, but I have a tool called `search_user` that can find her."* 
Instead of answering with text, the LLM responds with a **Tool Call Request** (e.g., `{"name": "search_user", "arguments": {"name": "Mia"}}`).

### 3. Executing the Tool
In `agent.py`, the code intercepts this tool call request:

```python
tool_call = message.tool_calls[0]
tool_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

result = await self.mcp.call_tool(tool_name, arguments)
```

**What happens inside `mcp.call_tool`?**
1.  The `MCPServerClient` (`backend/mcp_client.py`) spins up the FastMCP server (`mcp_server/server.py`).
2.  It sends the request to execute `search_user` with `{name: "Mia"}` over the Model Context Protocol.
3.  Inside `mcp_server/server.py`, the `@mcp.tool()` decorator catches this and triggers the `search_users` python function from `tools.py`.
4.  `tools.py` connects to the PostgreSQL database, runs a `SELECT ... WHERE first_name ILIKE '%Mia%'` query, and fetches the result.
5.  The MCP Server packages this database row into a standardized JSON response and sends it back to the `Agent`.

### 4. Second LLM Request (Generating the Final Answer)
Now the `Agent` has the database results (e.g., `[{"id": 3, "first_name": "Mia", "last_name": "Johnson", "email": "mia.j@example.com"}]`), but it needs to present this nicely to the user.

It appends two new messages to the conversation history:
1.  The LLM's original request to call the tool.
2.  The raw JSON result from the MCP tool execution.

It sends this updated conversation history back to the Groq LLM:
```python
final = self.llm.chat(messages)
return final.choices[0].message.content
```
The LLM reads the tool output, formats it into natural language (e.g., *"I found a user named Mia Johnson. Her email is mia.j@example.com."*), and returns this text.

### 5. Returning to the User
Finally, the `Agent.ask()` method returns this natural language string back to `test_agent.py`, which prints it to the terminal:
```python
print("\nAssistant:")
print(answer)
```
Then, the loop repeats, waiting for your next question!

---

## Summary of Component Connections

*   **`tests/test_agent.py`** ➔ Calls ➔ **`backend/agent.py`**
*   **`backend/agent.py`** ➔ Talks via API to ➔ **`backend/llm.py`** (Groq LLM)
*   **`backend/agent.py`** ➔ Talks via MCP to ➔ **`backend/mcp_client.py`**
*   **`backend/mcp_client.py`** ➔ Spawns & Communicates with ➔ **`mcp_server/server.py`**
*   **`mcp_server/server.py`** ➔ Invokes functions in ➔ **`mcp_server/tools.py`**
*   **`mcp_server/tools.py`** ➔ Queries ➔ **PostgreSQL Database** (`db.py`)
