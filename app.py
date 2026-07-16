import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Chatbot")
st.caption("FastAPI + Hugging Face + TiDB")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("""
    ### Features
    ✅ AI Chatbot
    ✅ Memory
    ✅ Guardrails
    ✅ TiDB Database
    ✅ FastAPI
    """)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
prompt = st.chat_input("Ask me anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "message": prompt
            }
        )

        answer = response.json()["response"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.write(answer)