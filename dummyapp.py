import streamlit as st
import requests
from gtts import gTTS
import PyPDF2
import tempfile
import time
import uuid

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🤖 AI Chatbot")
st.caption("FastAPI + Hugging Face + TiDB")

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# -----------------------------
# SIDEBAR (top part: static info + uploader)
# -----------------------------
with st.sidebar:
    st.header("🤖 AI Chatbot")
    st.markdown("### 🚀 Features")
    st.markdown("✅ Text Chat")
    st.markdown("✅ AI Voice")
    st.markdown("✅ PDF Upload")
    st.markdown("✅ Memory")
    st.markdown("✅ Guardrails")
    st.markdown("✅ Chat History")
    st.markdown("✅ FastAPI")
    st.markdown("✅ TiDB")
    st.success("🟢 AI Online")
    st.divider()

    uploaded_pdf = st.file_uploader("📄 Upload PDF", type=["pdf"])

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# READ PDF
# -----------------------------
pdf_text = ""

if uploaded_pdf is not None:
    reader = PyPDF2.PdfReader(uploaded_pdf)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

# -----------------------------
# DISPLAY EXISTING CHAT HISTORY
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
prompt = st.chat_input("💬 Ask me anything or ask questions from the uploaded PDF...")

response_time = None

if prompt:
    original_prompt = prompt

    if pdf_text:
        prompt = f"""You are a helpful AI Assistant.

Use the PDF content below to answer the user's question.

PDF:
{pdf_text[:5000]}

Question:
{original_prompt}
"""

    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": original_prompt})
    with st.chat_message("user"):
        st.write(original_prompt)

    # Call FastAPI (also measure response time here)
    with st.spinner("🤖 Thinking..."):
        start = time.time()
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message": prompt,
                    "session_id": st.session_state.session_id
                },
                timeout=30
            )
            response.raise_for_status()
            answer = response.json()["response"]
        except requests.exceptions.ConnectionError:
            answer = "❌ Unable to connect to FastAPI. Is the server running on port 8000?"
        except requests.exceptions.Timeout:
            answer = "❌ Request to FastAPI timed out."
        except requests.exceptions.HTTPError as e:
            answer = f"❌ FastAPI returned an error: {e} — {response.text}"
        except (KeyError, ValueError):
            answer = f"❌ Unexpected response format from FastAPI: {response.text}"
        except Exception as e:
            answer = f"❌ Unexpected error: {e}"
        response_time = round(time.time() - start, 2)

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Display AI response
    with st.chat_message("assistant"):
        st.write(answer)

        if response_time is not None:
            st.caption(f"⚡ Response Time: {response_time} sec")

        # Optional: read the answer aloud
        if st.button("🔊 Read aloud", key=f"tts_{len(st.session_state.messages)}"):
            try:
                tts = gTTS(text=answer, lang="en")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)
            except Exception as e:
                st.warning(f"Voice Error: {e}")

# -----------------------------
# SIDEBAR: STATS + DOWNLOAD (rendered after processing so counts are current)
# -----------------------------
with st.sidebar:
    st.metric("💬 Conversations", len(st.session_state.messages) // 2)
    st.metric("📄 PDF Loaded", "Yes" if uploaded_pdf else "No")

    chat_history = ""
    for msg in st.session_state.messages:
        chat_history += f"{msg['role'].upper()}\n"
        chat_history += f"{msg['content']}\n\n"

    st.download_button(
        "📥 Download Chat History",
        data=chat_history,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# -----------------------------------
# CHAT STATISTICS
# -----------------------------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "👤 User Messages",
        len([m for m in st.session_state.messages if m["role"] == "user"])
    )

with col2:
    st.metric(
        "🤖 AI Responses",
        len([m for m in st.session_state.messages if m["role"] == "assistant"])
    )

# -----------------------------------
# FOOTER
# -----------------------------------
st.divider()
st.caption("🚀 Developed using Streamlit • FastAPI • Hugging Face • TiDB")