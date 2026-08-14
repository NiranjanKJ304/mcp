import asyncio

import streamlit as st

from agent import GitHubAgent


st.set_page_config(
    page_title="GitHub MCP Agent",
    page_icon="🐙",
    layout="wide",
)


st.title("🐙 GitHub MCP Agent")

st.caption(
    "Groq + MCP + GitHub"
)


# --------------------------------
# Session state
# --------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "agent" not in st.session_state:

    st.session_state.agent = GitHubAgent()


# --------------------------------
# Display previous messages
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------
# Chat input
# --------------------------------

question = st.chat_input(
    "Ask something about GitHub..."
)


if question:

    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # Agent response

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking and using GitHub MCP..."
        ):

            try:

                answer = asyncio.run(
                    st.session_state.agent.ask(
                        question
                    )
                )

            except Exception as e:

                answer = (
                    f"Error: `{str(e)}`"
                )

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
