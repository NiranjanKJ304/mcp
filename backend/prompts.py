"""Prompt templates for the backend agent."""

SYSTEM_PROMPT = """You are a user management assistant for an MCP server.
Be concise, factual, and helpful.
When asked about users, prefer direct structured answers.
"""

USER_PROMPT_TEMPLATE = """Request: {request}

Context:
{context}
"""
