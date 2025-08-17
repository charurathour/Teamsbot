import streamlit as st
from agents.llm_agent import build_agent
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Agentic Chatbot", layout="wide")

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []
if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

agent = st.session_state.agent

# ---- Sidebar ----
st.sidebar.title("Software Installer")
apps = ["Zoom", "Slack", "VSCode", "Notepad++"]

for app in apps:
    if st.sidebar.button(app, use_container_width=True, key=f"btn_{app}"):
        user_text = f"Please install {app}"
        st.session_state.chat.append({"role": "user", "content": user_text})

        # Run agent
        state = {"messages": [HumanMessage(content=user_text)]}
        result = agent.invoke(state)

        # Append LLM/tool reply
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                st.session_state.chat.append({"role": "assistant", "content": msg.content})

        st.rerun()

# ---- Chat area ----
st.title("💬 Teams Chatbot")

for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ---- Chat input ----
if user_text := st.chat_input("Type your message..."):
    st.session_state.chat.append({"role": "user", "content": user_text})

    # Run agent
    state = {"messages": [HumanMessage(content=user_text)]}
    result = agent.invoke(state)

    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            st.session_state.chat.append({"role": "assistant", "content": msg.content})

    st.rerun()
