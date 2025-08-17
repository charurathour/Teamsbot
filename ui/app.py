# app.py
import streamlit as st

st.set_page_config(page_title="Teams Chatbot", page_icon="💬", layout="wide")

SOFTWARES = ["Zoom", "Slack", "VS Code", "Notepad++", "Postman", "Chrome"]

# --- Initialize chat history ---
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "assistant", "content": "Hi! Click a software button on the left or ask me anything."}
    ]

# --- Sidebar with clickable buttons ---
st.sidebar.title("🧰 Software")
st.sidebar.caption("Click a button to install software.")

for app in SOFTWARES:
    if st.sidebar.button(app, use_container_width=True, key=f"btn_{app}"):
        st.session_state.chat.append({"role": "user", "content": f"Install {app}."})
        st.session_state.chat.append({
            "role": "assistant",
            "content": f"Button clicked: **{app}**. (Installation flow would start here.)"
        })


# --- Main chat area ---
st.title("💬 Teams Chatbot")
st.caption("Your teams assistant with installation capabilities.")

# Display chat messages
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_text = st.chat_input("Type your message...")
if user_text:
    st.session_state.chat.append({"role": "user", "content": user_text})
    # Placeholder bot response (replace with LLM later)
    reply = f"You said: `{user_text}`. (Placeholder response.)"
    st.session_state.chat.append({"role": "assistant", "content": reply})
    st.rerun()
