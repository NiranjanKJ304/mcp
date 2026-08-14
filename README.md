# MCP Project - PostgreSQL and GitHub

This project is created for learning the Model Context Protocol (MCP) by integrating both a local database (PostgreSQL) and an external MCP server from GitHub.

## Tech Stack

* **Language**: Python
* **UI**: Streamlit
* **LLM Provider**: Groq (Model: `llama-3.3-70b-versatile`)
* **MCP Integration**: `fastmcp` for building and connecting to MCP servers
* **Databases/Services**:
  * Local PostgreSQL Database (Custom Local MCP Server)
  * GitHub (External MCP Server)

## Working Flow

1. **User Interaction**: The user submits a question through the Streamlit web interface.
2. **Agent Initialization**: The query is passed to an asynchronous Agent which connects to the configured MCP servers (Local PostgreSQL MCP and/or the external GitHub MCP Server).
3. **Tool Discovery**: The MCP servers expose their available tools to the Agent. These tools are formatted and provided to the Groq LLM.
4. **LLM Decision**: The Groq LLM analyzes the user's query and the available tools. If a tool call is required (e.g., fetching user data from the database or retrieving repository details from GitHub), the LLM requests a tool execution.
5. **Tool Execution**: The Agent intercepts the LLM's tool call request, executes the corresponding tool via the MCP client, and captures the result (or error).
6. **Final Response**: The tool's output is sent back to the Groq LLM, which synthesizes a final, human-readable response.
7. **Display**: The final response is presented to the user in the Streamlit chat interface.

## Run

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure your environment variables in `.env` (refer to `.env.example` for required keys like `GROQ_API_KEY` and `GITHUB_PERSONAL_ACCESS_TOKEN`).
4. Run the Streamlit application: `streamlit run streamlit_app.py`.
