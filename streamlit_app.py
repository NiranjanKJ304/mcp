import asyncio
import streamlit as st
from backend.agent import Agent

st.set_page_config(page_title="MCP Agent Chat", page_icon="🤖")

st.title("MCP Agent Chat")
st.markdown("Ask me questions, and I'll use tools to find the answers!")

# Initialize session state for Agent and messages
if "agent" not in st.session_state:
    st.session_state.agent = Agent()
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call agent and display response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Use asyncio.run to execute the async ask method
                response = asyncio.run(st.session_state.agent.ask(prompt))
                st.markdown(response)
                # Add assistant message to state
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
